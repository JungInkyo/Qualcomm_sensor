from btserver import BTServer
from btserver import BTError
from sensor import SensorServer

import argparse
import asyncore
import json
import logging
import sqlite3
from threading import Thread
from time import gmtime, sleep, strftime, time
import datetime

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv",
                        help="set output format: csv, json")
    parser.add_argument("--database", dest="database_name", default="air_pollution_data.db",
                        help="specify database file")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    bt_service_name = "Air Pollution Sensor"
    bt_server = BTServer(uuid, bt_service_name)

    # Create the server thread and run it
    bt_server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    bt_server_thread.daemon = True
    bt_server_thread.start()

    sensor_server = SensorServer(database_name=args.database_name)
    sensor_server.daemon = True
    sensor_server.start()

    try:
        db_conn = sqlite3.connect(args.database_name)
        db_cur = db_conn.cursor()
    except Exception as e:
        logger.error("Error connecting the database {}, reason: {}".format(args.database_name, e.message))

    while True:
        for client_handler in bt_server.active_client_handlers.copy():
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"
            sensor_output = sensor_server.get_sensor_output()
            raw = sensor_output.get('Temp', -1)
            v = 5 * 0.000244140625 * raw
            t = (1000 * v) - 642
            temp = t
            epoch_time = int(time())    # epoch time
            #real_time = time.localtime()  # real time
            SN1 = sensor_output.get('SN1', -1)      # random SN1 value
            SN2 = sensor_output.get('SN2', -1)       # random SN2 value
            SN3 = sensor_output.get('SN3', -1)       # random SN3 value
            SN4 = sensor_output.get('SN4', -1)     # random SN4 value
            PM25 = sensor_output.get('PM25', -1)    # random PM25 value

            msg = ""
            if args.output_format == "csv":
                msg = "realtime, %d, %f, %f, %f, %f, %f, %f" % (epoch_time, temp, SN1, SN2, SN3, SN4, PM25)
            elif args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': temp,
                          'NO2': SN1,
                          'O3': SN2,
                          'CO': SN3,
                          'SO2': SN4,
                          'PM25': PM25}
                msg = json.dumps(output)
            try:
                client_handler.send(msg + '\n')
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(3)
