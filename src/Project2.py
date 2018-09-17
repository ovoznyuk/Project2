from flask import Flask, render_template, json, request, redirect, url_for
from flaskext.mysql import MySQL
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data as web
import fix_yahoo_finance as yf
import quandl
import csv

import datetime

import os
import shutil

dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)
scriptpath = os.path.realpath(__file__)
print("Script path is : " + scriptpath)

app = Flask(__name__)
mysql = MySQL()

@app.route("/")
def main():

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home',  methods=['GET', 'POST'])
def home():

    return render_template('index4.html')


@app.route('/refresh', methods=['POST'])
def refresh():
    #    user =  request.form['username'];
    #    password = request.form['password'];

    ticker_file ='aapl'+ '.csv'
    try:
        print("Check Date bounds ...")
        startDate = request.form['analysisStart']
        endDate   = request.form['analysisEnd']
        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'VOVoli123'
        app.config['MYSQL_DATABASE_DB'] = 'finproject'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_PORT'] = 3306
        mysql.init_app(app)
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM stock_aapl where date = '"+startDate+"' OR date >= ( '"+startDate+"' - INTERVAL 5 DAY )")
        rows = cursor.fetchall()
        if cursor.rowcount < 1 :
            return "No data in Database, please Get Data from Yahoo! "
        cursor.execute("SELECT * FROM stock_aapl where date = '"+endDate+"' OR date <= ( '"+endDate+"' - INTERVAL 5 DAY )")
        rows = cursor.fetchall()
        if cursor.rowcount < 1 :
            return "No data in Database, please Get Data from Yahoo! "
        print("Get Data from Table ...")
        cursor.execute("SELECT * FROM stock_aapl WHERE date >= '"+startDate+"' AND date <= '"+endDate+"'")
        rows = cursor.fetchall()
        # open a file for writing
        aapl_data = open(ticker_file, 'w', newline='')
        # create the csv writer object
        csvwriter = csv.writer(aapl_data)
        header = ('Date', 'Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume')
        csvwriter.writerow(header)
        count = 0
        for row in rows:
            count = count + 1
            csv_val = (str(row[0])[:10], row[1], row[2], row[3], row[4], row[5], row[6])
            # csv_val = (str(date_stock)[:10], value['Open'], value['High'], value['Low'], value['Close'], value['Adj Close'], value['Volume'])
            csvwriter.writerow(csv_val)
        print(f'Processed: {count} lines.')
        aapl_data.close()
        if os.path.isfile(os.getcwd()+"\\static\data\\"+ticker_file):
            os.remove(os.getcwd()+"\\static\data\\"+ticker_file)
        shutil.copyfile(ticker_file, os.getcwd()+"\\static\data\\"+ticker_file)
        os.remove(ticker_file)
        cursor.close()
        conn.close()
        status = "OK"
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        pass
    return json.dumps({'message':str(status)})

@app.errorhandler(500)
def internal_error(error):

    return "500 error"

@app.route('/load', methods=['POST'])
def load():
    #    password = request.form['password'];
    #    startDate =  request.form['startDate'];
    #    endDate = request.form['endDate'];
    apple_name = "aapl.csv"
    try:
        # MySQL configurations for findatabase
        finDatabase = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'VOVoli123'
        app.config['MYSQL_DATABASE_DB'] = 'finproject'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_PORT'] = 3306
        finDatabase.init_app(app)
        # get cursor fo table
        conn = finDatabase.connect()
        apple_cursor =conn.cursor()
        print("Start loading!")
        apple_cursor.execute("DELETE FROM stock_aapl")
        # prepare to insert
        sql = "INSERT INTO stock_aapl (date, open, high, low, close, adj_close, volume) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        # open csv file
        csv_file = open(os.getcwd()+"\\static\data\\"+apple_name)
        with open(os.getcwd()+"\\static\data\\"+apple_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')
                    val = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    apple_cursor.execute(sql, val)
                    line_count += 1

            print(f'Processed {line_count} lines.')
        conn.commit()
    except Exception as e:
        return json.dumps({'error':str(e)})

    return "ok"


@app.route('/scrape', methods=['POST'])
def scrape():
    #    startDate =  request.form['startDate'];
    #    endDate = request.form['endDate'];
    try:
        startDate = request.form['analysisStart']
        endDate   = request.form['analysisEnd']
        print("Start scraping!")
        # We will look at stock prices for the days from 'startDate' to 'endDate'
        # start = datetime.date(2018,1,1)
        # end = datetime.date(2018,8,30)   #
        # end = datetime.date.today()

        # data = quandl.get("WIKI/AAPL", start_date=str(start), end_date=str(end), api_key='Q8BTAGMsvQSPVThQMgmU', order='desc')
        # apple = data.to_json(orient='index')
        # print(apple)
        # apple = get_data_quandle("AAPL", start, end)
        apple = get_data_yahoo("AAPL", startDate, endDate)
        if is_json(apple):
            status = put_in_table_aapl(apple)
            if status != "OK":
                apple = status
        else:
            print("Error :: "+apple)
            apple = "Yahoo! respond: "+apple

    except Exception as e:
        apple = json.dumps({'error':str(e)})
        print("Error!!!! ::  "+str(e))
    print("Scraping Done!")
    return apple

def put_in_table_aapl(json_data_apple):
    apple_name = "aapl.csv"
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
        conn = finDatabase.connect()
        apple_cursor =conn.cursor()
        apple_cursor.execute("DELETE FROM stock_aapl")
        # make file for csv
        # open a file for writing
        aapl_data = open(apple_name, 'w', newline='')
        # create the csv writer object
        csvwriter = csv.writer(aapl_data)
        header = ('Date', 'Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume')
        csvwriter.writerow(header)
        for key, value in json.loads(json_data_apple).items():
            date_stock = datetime.datetime.utcfromtimestamp(int(key)/1e3)
            sql = "INSERT INTO stock_aapl (date, open, high, low, close, adj_close, volume) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (date_stock, value['Open'], value['High'], value['Low'], value['Close'], value['Adj Close'], value['Volume'])
            apple_cursor.execute(sql, val)
            csv_val = (str(date_stock)[:10], value['Open'], value['High'], value['Low'], value['Close'], value['Adj Close'], value['Volume'])
            csvwriter.writerow(csv_val)

        aapl_data.close()
        conn.commit()
        if os.path.isfile(os.getcwd()+"\\static\data\\"+apple_name):
            os.remove(os.getcwd()+"\\static\data\\"+apple_name)
        shutil.copyfile(apple_name, os.getcwd()+"\\static\data\\"+apple_name)
        os.remove(apple_name)
        status = "OK"
    except Exception as e:
        status = e

    return status


def get_data_quandle(ticker, start_date, end_date):
    try:
        # Let's get Apple stock data; Apple's ticker symbol is AAPL
        data = quandl.get("WIKI/"+ticker, start_date=str(start_date), end_date=str(end_date), api_key='Q8BTAGMsvQSPVThQMgmU', order='desc')
        apple = data.to_json(orient='index')
        print(apple)
    except Exception as e:
        data = e.args[0]
    return data


def get_data_yahoo(ticker, startDate, endDate):
    yf.pdr_override()
    try:
        # Let's get Apple stock data; Apple's ticker symbol is AAPL
        apple = web.get_data_yahoo(ticker, startDate, endDate)
        data = json.dumps(json.loads(apple.to_json(orient='index')), indent=2)
    except Exception as e:
        data = e.args[0]
    return data


def get_data_url():
# https://www.quandl.com/api/v3/datasets/WIKI/DJI/data.csv?start_date=2018-01-01&end_date=2018-08-31&order=desc
    return "OK"

def is_json(test_json):
    try:
        json_object = json.loads(test_json)
    except ValueError as e:
        return False
    return True

if __name__ == "__main__":
    app.run()