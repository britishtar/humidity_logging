#!/usr/bin/env python3

from datetime import datetime as dt
import pytz
import time
import board
import adafruit_dht
import psutil
from helpers import init_dht, read_dht, add_entry

# Set variables appropriately:
dht_model = 22 # set to 11 for DHT11
logfile = "/home/pi/dhtlogs/DHT-{}.log".format(dt.now().strftime("%Y-%m-%d"))
timezone = pytz.timezone("America/New_York")
sampling_interval = 60.0 # number of seconds to wait between readings


timestamp = timezone.localize(dt.now()).strftime("%Y-%m-%d-%H:%M:%S") 
with open(logfile, "a") as f:
    f.write("Initialized logging script at {}".format(timestamp))
    f.write("\n")

# Initialize the dht device, with data pin connected to pin D4:
dhtDevice = init_dht(dht_model)

print("entering logging mode, sampling interval set to: {} seconds".format(sampling_interval))

while True:
    logfile = "/home/pi/dhtlogs/DHT-{}.log".format(dt.now().strftime("%Y-%m-%d"))
    try:
        # Print the values to the serial port
        values = read_dht(dhtDevice)
        temperature_f = values[0]
        humidity = values[1]
        timestamp = timezone.localize(dt.now()).strftime("%Y-%m-%d-%H:%M:%S") 
        add_entry(dt.now(), temperature_f, humidity)
        logstring = "{}, Temp: {} F, Humidity: {}%".format(timestamp, temperature_f, humidity)
        print(logstring)
        with open(logfile, "a") as f:
            f.write(logstring)
            f.write("\n")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(sampling_interval)
        continue
    except Exception as error:
        dhtDevice.exit()
        with open(logfile, "a") as f:
            f.write("ERROR occurred in logging script: {}".format(error))
            f.write("\n")
        raise error

    time.sleep(sampling_interval)
