from abc import abstractmethod
from collections import OrderedDict
import datetime

from Phidgets.PhidgetException import PhidgetException

import Phidgets.Devices.GPS

from mmo.device.device import Device


class GpsLike(Device):
    @abstractmethod
    def get_fix(self):
        pass


class Gps(GpsLike):
    def __init__(self):
        gps = Phidgets.Devices.GPS.GPS()
        self.gps = gps
        gps.setOnAttachHandler(self.attach_handler)
        gps.setOnDetachHandler(self.detach_handler)
        gps.openPhidget()
        try:
            gps.waitForAttach(1000)
        except PhidgetException:
            print "WARNING: No GPS connected"

    def get_fix(self):
        if not self.gps.isAttached():
            print "WARNING: No GPS Attached"
            return GpsFix()
        if not self.gps.getPositionFixStatus():
            # No good GPS fix
            return GpsFix()

        t = self.gps.getTime()
        d = self.gps.getDate()
        timestamp = datetime.datetime(d.year, d.month, d.day, t.hour, t.min, t.sec, t.ms * 1000)

        return GpsFix(timestamp=timestamp,
                      latitude=self.gps.getLatitude(),
                      longitude=self.gps.getLongitude(),
                      altitude=self.gps.getAltitude(),
                      heading=self.gps.getHeading(),
                      velocity=self.gps.getVelocity())


class GpsFix(object):
    """
    Contains info from a GPS position
    """

    def __init__(self, timestamp=None, latitude=None, longitude=None, altitude=None, heading=None, velocity=None):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading
        self.velocity = velocity

    def __str__(self):
        return "t: {}, lat: {}, lon: {}, alt: {}, hdg: {}, vel: {}" \
            .format(self.timestamp, self.latitude, self.longitude, self.altitude, self.heading, self.velocity)

    def as_dict(self):
        return OrderedDict((
            ("gps_time", self.timestamp),
            ("latitude", self.latitude),
            ("longitude", self.longitude),
            ("altitude", self.altitude),
            ("heading", self.heading),
            ("velocity", self.velocity)))