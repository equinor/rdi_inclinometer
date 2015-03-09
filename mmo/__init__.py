from datetime import datetime, timedelta
from mmo.axis_translator import *
from mmo.database import Database


class ConfigType(object):
    """
    :type axis_translator AxisTranslator
    """
    height = 0
    axis_translator = None
    gps_timedelta = timedelta(seconds=10)

    def __init__(self):
        self.refresh()

    @staticmethod
    def get_sampling_rate():
        """
        8 is the lowest allowed number to use with the compass
        """
        return 8

    def refresh(self):
        db_config = Database.get_config()
        self.height = int(db_config['height'])

        axis = db_config['selectedAxis']
        self.axis_translator = translator_dict[axis]


class StatusType(object):
    spatial_connected = False
    gps_connected = False
    last_gps_fix = None
    last_stored_gps_time = datetime(1970, 1, 1)

    def get_gps_status(self):
        if self.gps_connected:
            return "Connected"
        return "Disconnected"

    def get_spatial_status(self):
        if self.spatial_connected:
            return "Connected"
        return "Disconnected"

    def update_position(self, gps_fix):
        self.last_gps_fix = gps_fix
        if gps_fix.timestamp - self.last_stored_gps_time > config.gps_timedelta:
            self.last_stored_gps_time = gps_fix.timestamp
            Database.store_position(gps_fix.timestamp, gps_fix.latitude, gps_fix.longitude, gps_fix.altitude)

    @staticmethod
    def get_system_time():
        return datetime.utcnow()


config = ConfigType()

status = StatusType()