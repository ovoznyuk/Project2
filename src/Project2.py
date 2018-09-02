from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data as web
import fix_yahoo_finance as yf

import datetime

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VOVoli123'
app.config['MYSQL_DATABASE_DB'] = 'world'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

@app.route("/")
def main():

    return render_template('index3.html')

@app.route('/refresh', methods=['POST'])
def refresh():
#    user =  request.form['username'];
#    password = request.form['password'];

    cities = 'None'
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM city")
        rows = cursor.fetchall()

        # Convert query to objects of key-value pairs
        objects_list = []
        count = 0
        for row in rows:
            count = count + 1
            if count < 10 :
                print(" %2d\t ID=%3d,\t Name=%15s" % (count, row[0], row[1]))

            d = [(row[0]), (row[1]), (row[2]), (row[3]), (row[4])]
            objects_list.append(d)
        cities = json.dumps(objects_list)
#        cities = json.dumps(data)
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
    return cities

@app.errorhandler(500)
def internal_error(error):

    return "500 error"

@app.route('/scrape', methods=['POST'])
def scrape():
    #    startDate =  request.form['startDate'];
    #    endDate = request.form['endDate'];
    try:
        print("Start!")
        # We will look at stock prices for 7 business days, starting from Aug 20
        start = datetime.datetime(2018,8,20)
        end = datetime.datetime(2018,8,28)   #datetime.date.today()

        apple = getDadaYahoo("AAPL", start, end)
        if is_json(apple):
            status = putInTableAAPL(apple)
            if status != "OK":
                apple = status
        else:
            apple = "Error, no JSON in answer!!!"

    except Exception as e:
        apple = json.dumps({'error':str(e)})

    return apple

def putInTableAAPL(jsonData_apple):
    try:
        finDatabase = MySQL()
        # MySQL configurations for findatabase
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'VOVoli123'
        app.config['MYSQL_DATABASE_DB'] = 'finproject'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_PORT'] = 3306
        finDatabase.init_app(app)
        # get cursor fo table
        conn = mysql.connect()
        apple_cursor =conn.cursor()
        apple_cursor.execute("DELETE FROM stock_aapl")
        for key, value in json.loads(jsonData_apple).items():
            date_stuck = datetime.datetime.utcfromtimestamp(int(key)/1e3)
            sql = "INSERT INTO stock_aapl (date, open, high, low, close, adj_close, volume) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (date_stuck, value['Open'], value['High'], value['Low'], value['Close'], value['Adj Close'], value['Volume'])
            apple_cursor.execute(sql, val)
        conn.commit()
        status = "OK"
    except Exception as e:
        status = e

    return status


def getDadaYahoo(ticker, startDate, endDate):
    yf.pdr_override()
    try:
        # Let's get Apple stock data; Apple's ticker symbol is AAPL
        apple = web.get_data_yahoo(ticker, startDate, endDate)
        data = json.dumps(json.loads(apple.to_json(orient='index')), indent=2)
    except Exception as e:
        data = e.args[0]
    return data

def is_json(test_json):
    try:
        json_object = json.loads(test_json)
    except ValueError as e:
        return False
    return True

if __name__ == "__main__":
    app.run()