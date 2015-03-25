from mmo.database import Database

from mmo.storage import Storage


class DatabaseStorage(Storage):
    def store(self, host_name, gps_fix, gyro, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        Database.store_observation(host_name, gps_fix, gyro, accelerometer_fix, compass_fix, roll_pitch_yaw, typ)

    def dump_list(self, limit=1000000, page=1):
        return Database.dump_observations(limit=limit, page=page)