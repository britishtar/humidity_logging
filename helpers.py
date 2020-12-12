# helper functions

import adafruit_dht
import board
import time
import psutil
import sqlite3 as lite
import sys
import os

def init_dht(model=22):
    model = int(model)
    print(model)
    flag = True
    while flag:
        try:
            print("attempting to initialize device...")
            if model == int(22):
                print("DHT22...")
                dhtDevice = adafruit_dht.DHT22(board.D4)
            elif model == int(11):
                print("DHT11...")
                dhtDevice = adafruit_dht.DHT11(board.D4)
            else:
                print("incorrect DHT model number--enter '11' or '22'")
                return None
            dhtDevice.temperature
            print("successfully initialized DHT" + str(model))

        except RuntimeError as error:
            print(error.args[0])
            print("failed to initialize, cleaning up libgpio processes...")
            for p in psutil.process_iter():
                if p.name()[:8] == 'libgpiod':
                    print("killing {} (pid: {})".format(p.name(), p.pid))
                    p.kill()
            time.sleep(5)
            continue
        flag = False
    return dhtDevice


def read_dht(dhtDevice, deg='F'):
    while True:
        try:
            t = dhtDevice.temperature
            h = dhtDevice.humidity
            if deg == 'F':
                t = t * (9 / 5) + 32
            return (t, h)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)


def create_table(location, debug=False):
    # Create DHT_data table if it doesn't exist already
    con = lite.connect(os.path.join(location, 'sensorsData.db'))
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
    return con


def add_entry(db, timestamp, temp, hum, debug=False):
    # Add a temp/humidity reading to the database
    with db as con:
        cur = con.cursor()
        if debug:
            print("Adding DHT reading to DHT_data table: ", timestamp, temp, hum)
        cur.execute("INSERT INTO DHT_data VALUES((?), (?), (?))", (timestamp, temp, hum))