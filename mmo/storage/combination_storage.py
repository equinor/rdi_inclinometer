from mmo.storage import Storage


class CombinationStorage(Storage):
    def __init__(self, *storages):
        super(self.__class__, self).__init__()
        self.storages = storages

    def dump_csv(self):
        return self.storages[0].dump_csv()

    def dump_table(self):
        return self.storages[0].dump_table()

    def dump_list(self, limit=1000000, page=1):
        return self.storages[0].dump_list(limit=limit, page=page)

    def store(self, host_name, gps_fix, gyro, gyro_momentary, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        sample_id = None
        for storage in self.storages:
            temp_id = storage.store(host_name=host_name,
                                    gps_fix=gps_fix,
                                    gyro=gyro,
                                    gyro_momentary=gyro_momentary,
                                    accelerometer_fix=accelerometer_fix,
                                    compass_fix=compass_fix,
                                    roll_pitch_yaw=roll_pitch_yaw,
                                    typ=typ)
            if temp_id is not None:
                sample_id = temp_id
        return sample_id
