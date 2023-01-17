import build_table
from flask import Flask
import sqlite3
from flask import Flask, render_template
import html
import day_pages


server = Flask(__name__)

def days_lst():
   days_lst = build_table.days_lst
   return days_lst

def show_table():
   con = sqlite3.connect('NASA.db')
   con.row_factory = sqlite3.Row
   return con

@server.route('/')
def index():
   conn = show_table()
   martian_weather = conn.execute('SELECT * FROM martian_weather').fetchall()
   conn.close()
   return render_template('base.html', mars_weather=martian_weather)


@server.route('/data.html')
def data():
   conn = show_table()
   martian_weather = conn.execute('SELECT * FROM martian_weather').fetchall()
   conn.close()
   return render_template('data.html', mars_weather=martian_weather, days_lst =days_lst())


@server.route('/about.html')
def about():
   return render_template('about.html')

@server.route('/675.html')
def six_seven_five():
   return render_template('675.html')

@server.route('/676.html')
def six_seven_six():
   return render_template('676.html')

@server.route('/677.html')
def six_seven_seven():
   return render_template('677.html')

@server.route('/678.html')
def six_seven_eight():
   return render_template('678.html')

@server.route('/679.html')
def six_seven_nine():
   return render_template('679.html')

@server.route('/680.html')
def six_eighty():
   return render_template('680.html')
   
@server.route('/681.html')
def six_eight_one():
   return render_template('681.html')

day_pages.create_day_file()

server.run()
