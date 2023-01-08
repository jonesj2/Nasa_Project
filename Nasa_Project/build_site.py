import main_run
from flask import Flask
import sqlite3
from flask import Flask, render_template
import html


server = Flask(__name__)

@server.route('/')
def show_table():
   con = sqlite3.connect("'NASA_database'.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from martian_weather")
   
   rows = cur.fetchall()
   return render_template("server.html", rows=rows)



if __name__ == '__main__':
   server.run()