from mmo.database import Database

from mmo.storage import Storage


class DatabaseStorage(Storage):
    def store(self, host_name, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        Database.store_observation(host_name, gps_fix, gyro, accelerometer_fix, compass_fix, typ)

    def dump_list(self):
        return Database.dump_observations()