from mmo.storage import Storage


class CombinationStorage(Storage):
    def __init__(self, *storages):
        self.storages = storages

    def dump_csv(self):
        return self.storages[0].dump_csv()

    def dump_table(self):
        return self.storages[0].dump_table()

    def dump_list(self):
        return self.storages[0].dump_list()

    def store(self, gps_fix, gyro, accelerometer_fix, compass_fix, typ):
        for storage in self.storages:
            storage.store(gps_fix, gyro, accelerometer_fix, compass_fix, typ)