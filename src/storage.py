from collections import OrderedDict
import datetime
from os.path import exists
import csv
import sqlite3

from device.compass import CompassFix


class Storage:
    """
    Handles storing measurements from sensors
    """

    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        pass


class SqlStorage:
    def __init__(self, file_path):
        conn = sqlite3.connect(file_path)
        conn.row_factory = sqlite3.Row


    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        pass


class CsvStorage(Storage):
    def __init__(self, file_path, print_to_console=True):
        self.print_to_console = print_to_console
        self.file_path = file_path

    def dump_csv(self):
        with open(self.file_path, "r") as f:
            return f.read()

    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        """
        :type compass_fix: CompassFix
        :type typ: str
        :type accelerometer_fix: AccelerometerFix
        :type gyro: Gyro
        :type gps_fix: GpsFix
        """
        date = datetime.datetime.now()

        data_dict = OrderedDict()
        data_dict["Button_type"] = typ
        data_dict["System_time"] = date
        data_dict.update(gps_fix.as_dict())
        data_dict.update(gyro.as_dict())
        data_dict.update(accelerometer_fix.as_dict())
        data_dict.update(compass_fix.as_dict())

        if self.print_to_console:
            print "Writing csv: {}".format(data_dict)

        file_already_exists = exists(self.file_path)
        with open(self.file_path, "a") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=data_dict.keys())
            if not file_already_exists:
                writer.writeheader()
            writer.writerow(data_dict)