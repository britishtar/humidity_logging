import sqlite3 as lite
import sys


def create_table(debug=False):
    # Create DHT_data table if it doesn't exist already
    con = lite.connect('sensorsData.db')
    with con:
        cur = con.cursor()
        #if table 'DHT_data' exists:
        try:
            cur.execute("CREATE TABLE DHT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
            if debug:
                print("Created DHT_data table")
        except:
            if debug:
                print("DHT_data table already exists")


def add_entry(timestamp, temp, hum, debug=False):
    # Ensure the 'sensorsData.db' exists:
    create_table()
    # Add a temp/humidity reading to the database
    con = lite.connect('sensorsData.db')
    with con:
        cur = con.cursor()
        if debug:
            print("Adding DHT reading to DHT_data table: ", timestamp, temp, hum)
        cur.execute("INSERT INTO DHT_data VALUES((?), (?), (?))", (timestamp, temp, hum))


