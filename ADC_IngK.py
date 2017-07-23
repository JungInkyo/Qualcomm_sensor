from time import sleep #import sleep

while True: #it runs all the time
    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    v = (5000*raw) / 4096
    t = v -642
    print t
    sleep(1)