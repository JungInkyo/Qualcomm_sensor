from btserver import BTServer
from bterror import BTError

import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time
import datetime

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    while True:
        for client_handler in server.active_client_handlers.copy():
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"
            #real_time = datetime.datetime.now()  #real time
            epoch_time = int(time()) # epoch time
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            v = 5 * 0.000244140625 * raw
            t = (1000 * v) - 642
            temp = t     # random temperature
            SN1 = uniform(20, 50)  # random SN1 value
            SN2 = uniform(20, 50)  # random SN2 value
            SN3 = uniform(20, 50)  # random SN3 value
            SN4 = uniform(20, 50)  # random SN4 value
            PM25 = uniform(20, 50)  # random PM25 value
            #SN1 = uniform(40, 50)       # random SN1 value
            #SN2 = uniform(60, 70)       # random SN2 value
            #SN3 = uniform(80, 90)       # random SN3 value
            #SN4 = uniform(100, 110)     # random SN4 value
            #PM25 = uniform(120, 130)    # random PM25 value

            msg = ""
            if args.output_format == "csv":
                #msg = "%d, %f, %f, %f, %f, %f, %f" % (epoch_time, temp, SN1, SN2, SN3, SN4, PM25)
                msg = "%d, %s, %f, %f, %f, %f, %f, %f" % (0,epoch_time, temp, SN1, SN2, SN3, SN4, PM25)
            elif args.output_format == "json":
                output = {'type': 0,
                          'time': epoch_time,
                          'CO': SN1,
                          'SO2': SN2,
                          'NO2': SN3,
                          'O3': SN4,
                          'PM25': PM25}
                msg = json.dumps(output)
            try:
                client_handler.send(msg + '\n')
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(3)
