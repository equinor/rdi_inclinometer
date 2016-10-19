from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime, timedelta
from os import system
from mmo.axis_translator import *
from mmo.database import Database


class ConfigType(object):
    """
    :type axis_translator AxisTranslator
    """
    height = 0
    axis_translator = None
    gps_timedelta = timedelta(seconds=10)
    sampling_rate = 8 # Varies between 4 and 1000
    average_sample_count = 20
    observations_to_show_on_main_page = 200

    def __init__(self):
        self.refresh()

    def refresh(self):
        db_config = Database.get_config()
        self.height = int(db_config['height'])
        self.sampling_rate = int(db_config['samplingRate'])
        #self.average_sample_count = int(db_config['averageSampleCount'])
        self.observations_to_show_on_main_page = int(db_config['observationsToShowOnMainPage'])

        axis = db_config['selectedAxis']
        self.axis_translator = translator_dict[axis]

    @staticmethod
    def get_num_records():
        return Database.get_num_observations()


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

    def update_system_time_from_gps(self):
        gps_time_string = self.last_gps_fix.timestamp.isoformat()
        return_code = system("sudo date -s '{}'".format(gps_time_string))
        return return_code == 0

config = ConfigType()

status = StatusType()
