from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import collections

mysql = MySQL()
app = Flask(__name__)

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
    return cities;

@app.errorhandler(500)
def internal_error(error):

    return "500 error"

@app.route('/scrape', methods=['POST'])
def scrape():
    #    startDate =  request.form['startDate'];
    #    endDate = request.form['endDate'];
    apple = "none"
    try:
        import pandas as pd
        pd.core.common.is_list_like = pd.api.types.is_list_like
        from pandas_datareader import data as web
        import datetime
        import fix_yahoo_finance as yf

        yf.pdr_override()

        # We will look at stock prices for 7 business days, starting from Aug 20
        start = datetime.datetime(2018,8,20)
        end = datetime.datetime(2018,8,28)   #datetime.date.today()

        # Let's get Apple stock data; Apple's ticker symbol is AAPL
        apple = web.get_data_yahoo("AAPL", start, end)

        # apple = json.dumps(json.loads(apple.reset_index().to_json(orient='records')), indent=2)
        apple = json.dumps(json.loads(apple.to_json(orient='index')), indent=2)
        # apple = json.dumps(apple)

        print(start)

        count = 0
        for row in apple:
            count = count + 1
            if count < 10 :
                print(row)
                # print(" %2d\t ID=%3d,\t Name=%15s" % (count, row[0], row[1]))

        print(end)
        # print(apple)

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        print(apple)
    return apple;


if __name__ == "__main__":
    app.run()