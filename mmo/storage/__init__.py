class Storage:
    """
    Handles storing measurements from sensors
    """

    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        pass


from csv_storage import CsvStorage
from database_storage import DatabaseStorage