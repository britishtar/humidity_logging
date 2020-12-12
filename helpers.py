# helper functions

import adafruit_dht
import board
import time
import psutil

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


