import build_table
import sqlite3

#Connect SQL database
cnx = sqlite3.connect('NASA.db')
cursor = cnx.cursor()

#make a weather table in the database (only need to run once, then comment function out)
cursor.execute("CREATE TABLE IF NOT EXISTS martian_weather (Days VARCHAR(255) NOT NULL, Measure VARCHAR(255) NOT NULL, Reading VARCHAR(255) NOT NULL)")
cursor.close
#Put weather information in the weather table
build_table.new_frame.to_sql('martian_weather', cnx, if_exists='replace', index = False)


days = build_table.days_lst


def create_day_file():
    cnx = sqlite3.connect('NASA.db')
    cursor = cnx.cursor()
    for day in days:
        cursor.execute("SELECT * FROM martian_weather WHERE Days LIKE (?) ORDER BY Days", (day,))
        result = cursor.fetchall()

        with open ('templates/'+(day)+'.html', 'w') as create_file:
            create_file.write("{% extends 'base.html' %}{% block content %}")
            for row in result:
                create_file.write(str(row))
                create_file.write("<p style='color: white;'> </p>")
            create_file.write("{% endblock %}")
        
            create_file.close

create_day_file()

cnx.commit()
cursor.close()
cnx.close()
