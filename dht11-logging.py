#!/usr/bin/env python3

from datetime import datetime as dt
import pytz
import time
import board
import adafruit_dht
import psutil

# Set variables appropriately:
logfile = "/home/pi/dhtlogs/DHT-{}.log".format(dt.now().strftime("%Y-%m-%d"))
timezone = pytz.timezone("America/New_York")
sampling_interval = 30.0 # number of seconds to wait betweek read attempts


timestamp = timezone.localize(dt.now()).strftime("%Y-%m-%d-%H:%M:%S") 
with open(logfile, "a") as f:
    f.write("Initialized logging script at {}".format(timestamp))
    f.write("\n")

# Initial the dht device, with data pin connected to:
flag = True
while flag:
    try:
        print("trying to initialize device...")
        dhtDevice = adafruit_dht.DHT11(board.D4)
        dhtDevice.temperature 
        print("successfully initialized DHT11")
    except:
        for p in psutil.process_iter():
            if p.name()[:8] == 'libgpiod':
                print("killing {} (pid: {})".format(p.name(), p.pid))
                p.kill()
        time.sleep(5)
        continue
    flag = False

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

print("entering logging mode, sampling interval set to: {} seconds".format(sampling_interval))

while True:
    logfile = "/home/pi/dhtlogs/DHT-{}.log".format(dt.now().strftime("%Y-%m-%d"))
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        timestamp = timezone.localize(dt.now()).strftime("%Y-%m-%d-%H:%M:%S") 
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
