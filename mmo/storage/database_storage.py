from mmo.database import Database

from mmo.storage import Storage


class DatabaseStorage(Storage):
    def store(self, host_name, gps_fix, gyro, gyro_momentary, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        return Database.store_observation(host_name, gps_fix, gyro, gyro_momentary, accelerometer_fix, compass_fix,
                                          roll_pitch_yaw, typ)

    def dump_list(self, limit=1000000, page=1):
        return Database.dump_observations(limit=limit, page=page)
    
    def get(self, sample_id):
        return Database.get_observation(sample_id)
