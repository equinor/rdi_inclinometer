import datetime
from os.path import exists
from accelerometer import AccelerometerFix
from compass import CompassFix
from gyro import Gyro
from gps import GpsFix


class Storage:
    """
    Handles storing measurements from sensors
    """
    pass


class CsvStorage(Storage):
    def __init__(self, file_path, print_to_console=True):
        self.print_to_console = print_to_console
        self.file_path = file_path

        file_already_exists = exists(file_path)

        self.file_handle = open(file_path, "a")

        if not file_already_exists:
            self.file_handle.write(self.csv_headers() + "\n")

    @staticmethod
    def csv_headers():
        return "{};{};{}{}{}{}".format("Button_type",
                                       "System_time",
                                       GpsFix.csv_headers(),
                                       Gyro.csv_headers(),
                                       AccelerometerFix.csv_headers(),
                                       CompassFix.csv_headers())

    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        """
        :type compass_fix: CompassFix
        :type typ: str
        :type accelerometer_fix: AccelerometerFix
        :type gyro: Gyro
        :type gps_fix: GpsFix
        """
        # self.file_handle.write
        date = datetime.datetime.now()
        csv_line = "{};{};{}{}{}{}".format(typ,
                                           date,
                                           gps_fix.to_csv(),
                                           gyro.to_csv(),
                                           accelerometer_fix.to_csv(),
                                           compass_fix.to_csv())
        if self.print_to_console:
            print csv_line
        self.file_handle.write(csv_line + "\n")