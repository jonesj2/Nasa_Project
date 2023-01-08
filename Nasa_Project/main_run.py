import requests
import pandas as pd
import sqlite3
from flask import Flask, render_template
import html

 

#User should type in terminal what information they want

#API information
key = 'qza17H6uNk0zx0oqjeSJsWizFddA9OVYNQISNdSe'
url = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight_temperature&wind&pressure&feedtype=json&ver=1.0&key={0}".format(key)
response = requests.request("GET", url)

#Access data by extracting values
data = response.json()


#flattening into a pandas dataframe
frame = pd.json_normalize(data, sep='_')
our_dicti = frame.to_dict(orient='index')[0]


#converting keys to a list of strings so SQL will accept parameters
final_dicti_keys = []

def keys_to_strings(dicti_keys):
    for key in dicti_keys:
        if type(key) == list:
            key = " ".join(map(str, key))
        final_dicti_keys.append(key)
    return(final_dicti_keys)


#converting values to a list of strings so SQL will accept parameters
final_dicti_values = []

def values_to_strings(dicti_values):
    for value in dicti_values:
        if type(value) == list:
            value = (" ".join(map(str, value)))
        final_dicti_values.append(value)
    return(final_dicti_values)


#Run both conversions
keys_to_strings(our_dicti.keys())
values_to_strings(our_dicti.values())


#converting the key value pairs back into a dictioanry
final_dct = {'measurements': final_dicti_keys, 'values': final_dicti_values}

#making a dataframe
days_lst = final_dicti_values[0].split(" ")

days_column = []

for x in final_dicti_keys: 
    if x == 'sol_keys':   
        days_column.append('sol_keys')
    for y in days_lst: 
        if y in x:
            days_column.append(y)
    if '682' in x or '674' in x:
        days_column.append("outside of test days")

days_column.append("null")
days_column.append("null")

new_frame = pd.DataFrame.from_dict(final_dct)
new_frame.insert(0, "Days", days_column, True) 


#Connect MySQL database
cnx = sqlite3.connect('NASA_database')
cursor = cnx.cursor()

#make a weather table in the database (only need to run once, then comment function out)
cursor.execute("CREATE TABLE IF NOT EXISTS martian_weather (Days VARCHAR(255) NOT NULL, Measure VARCHAR(255) NOT NULL, Reading VARCHAR(255) NOT NULL)")

#Put weather information in the weather table
new_frame.to_sql('martian_weather', cnx, if_exists='replace', index = False)

cursor.execute('''  SELECT * FROM martian_weather''')

for row in cursor.fetchall():
    print (row)


cnx.commit()
cursor.close()
cnx.close()
