from mmo.database import Database


class Config(object):
    height = 0

    def __init__(self):
        self.refresh()


    @staticmethod
    def get_sampling_rate():
        """
        8 is the lowest allowed number to use with the compass
        """
        return 8

    def get_height(self):
        return self.height

    def refresh(self):
        self.height = Database.get_config()['height']


class Status(object):
    spatial_connected = False
    gps_connected = False

config = Config()

status = Status()