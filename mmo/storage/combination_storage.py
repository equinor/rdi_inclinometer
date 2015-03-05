from mmo.storage import Storage


class CombinationStorage(Storage):
    def __init__(self, *storages):
        super(self.__class__, self).__init__()
        self.storages = storages

    def dump_csv(self):
        return self.storages[0].dump_csv()

    def dump_table(self):
        return self.storages[0].dump_table()

    def dump_list(self):
        return self.storages[0].dump_list()

    def store(self, host_name, gps_fix, gyro, accelerometer_fix, compass_fix, roll_pitch_yaw, typ):
        for storage in self.storages:
            storage.store(host_name=host_name,
                          gps_fix=gps_fix,
                          gyro=gyro,
                          accelerometer_fix=accelerometer_fix,
                          compass_fix=compass_fix,
                          roll_pitch_yaw=roll_pitch_yaw,
                          typ=typ)