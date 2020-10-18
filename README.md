# Humidity Logging with the DHT11

Script adapted from: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

Pinout from: https://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

## Requirements

This script is tested on the Raspberry Pi zero running the minimal (headless) installation of Raspberry Pi OS (Buster, kernel version 5.4.51+)

Requires the following:
+ python3 (version 3.5+)
+ python3-pip
+ libgpiod2
+ adafruit-circuitpython-dht (install with pip)
+ pytz (install with pip)

Install dependencies as follows:

```shell
$ sudo apt-get install python3 python3-pip libgpiod2
$ pip3 install adafruit-circuitpython-dht pytz
```

## Instructions:

### Connect the DHT11 to your Raspberry Pi's GPIO header

Use the following pinout:
+ 'VCC' to one of the 5V pins
+ 'data' to GPIO pin 4
+ 'gnd' to one of the ground pins

*NOTE: make sure you get the power and ground leads right, or you risk creating a short-circuit and frying your Pi!*


### Configure the script and add Cronjob

Edit "dht11-logging.py":

+ change 'logfile' path to desired location
+ change 'timezone' appropriately
+ change 'sampling_interval' to desired--I'm told the DHT11 is only accurate ~1 reading per minute

Add a cron job to start the script on boot:

```shell
$ vim crontab -e
```

Add the following line to the end:

```
@reboot </path/to>/dht11-logging.py &
```

+ Replace </path/to> with the full pathname for the script
+ Make sure the ampersand is at the end, this will allow boot to continue while the script is running
+ Make sure this is done with the pi user, not sudo/root.


