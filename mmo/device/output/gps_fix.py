from collections import OrderedDict
from datetime import datetime
from Phidgets.PhidgetException import PhidgetException


def wrap_exception_with_none(op):
    try:
        return op()
    except PhidgetException:
        return None


class GpsFix(object):
    """
    Contains info from a GPS position
    """

    def __init__(self, timestamp=None, latitude=None, longitude=None, altitude=None, heading=None, velocity=None):
        """
        :type timestamp: datetime.datetime
        """
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

    @staticmethod
    def from_phidget(gps):
        t = gps.getTime()
        d = gps.getDate()
        timestamp = datetime(d.year, d.month, d.day, t.hour, t.min, t.sec, t.ms * 1000)
        return GpsFix(timestamp=timestamp,
                      latitude=gps.getLatitude(),
                      longitude=gps.getLongitude(),
                      altitude=gps.getAltitude(),
                      heading=wrap_exception_with_none(gps.getHeading),
                      velocity=wrap_exception_with_none(gps.getVelocity))