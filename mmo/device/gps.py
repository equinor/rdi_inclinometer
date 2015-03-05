from Phidgets.Devices.GPS import GPS as GpsPhidget
from abc import abstractmethod
from collections import OrderedDict
import datetime

from Phidgets.PhidgetException import PhidgetException

from mmo.device.device import Device
import mmo


class GpsLike(Device):
    @abstractmethod
    def get_fix(self):
        pass


class Gps(GpsLike):
    lastPositionTime = datetime.datetime(1970, 1, 1)

    def __init__(self):
        gps = GpsPhidget()
        self.gps = gps
        gps.setOnAttachHandler(self.attach_handler)
        gps.setOnDetachHandler(self.detach_handler)
        gps.setOnPositionChangeHandler(self.position_change_handler)
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

        return GpsFix.from_phidget(self.gps)

    def attach_handler(self, event):
        super(Gps, self).attach_handler(event)
        mmo.status.gps_connected = True

    def detach_handler(self, event):
        super(Gps, self).detach_handler(event)
        mmo.status.gps_connected = False
        print "WARNING: GPS disconnected"

    def position_change_handler(self, event):
        fix = GpsFix.from_phidget(self.gps)
        mmo.status.update_position(fix)


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
        timestamp = datetime.datetime(d.year, d.month, d.day, t.hour, t.min, t.sec, t.ms * 1000)
        return GpsFix(timestamp=timestamp,
                      latitude=gps.getLatitude(),
                      longitude=gps.getLongitude(),
                      altitude=gps.getAltitude(),
                      heading=gps.getHeading(),
                      velocity=gps.getVelocity())