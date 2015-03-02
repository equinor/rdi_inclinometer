from collections import OrderedDict
import datetime
from os.path import exists
import csv

from mmo.storage import Storage


class CsvStorage(Storage):
    def __init__(self, file_path, print_to_console=True):
        super(self.__class__, self).__init__()
        self.print_to_console = print_to_console
        self.file_path = file_path

    def dump_csv(self):
        with open(self.file_path, "r") as f:
            return f.read()

    def dump_list(self):
        with open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def store(self, host_name, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        date = datetime.datetime.now()

        data_dict = OrderedDict()
        data_dict["Host_name"] = host_name
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