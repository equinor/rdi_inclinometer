from Phidgets.PhidgetException import PhidgetException
from mmo import config
from collections import OrderedDict
from math import acos, pi, radians, tan


class AccelerometerFix:
    dip = None
    dist = None
    height = None

    def __init__(self, a0=None, a1=None, a2=None):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.dip = self.dip_angle()
        self.dist = self.distance()
        self.height = config.height

    def __str__(self):
        return "a0={}, a1={}, a2={}, dip={}".format(self.a0, self.a1, self.a2, self.dip)

    def dip_angle(self):
        a0, a1, a2 = config.axis_translator.translate(self.a0, self.a1, self.a2)
        print "{} {} {} becomes {} {} {}".format(self.a0, self.a1, self.a2, a0, a1, a2)
        if a1 is None:
            return None
        # l = sqrt(self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2)
        r1 = acos(max(-1, min(1, a1)))

        dip1 = 90 - (r1 * 180 / pi)
        return dip1

    def distance(self):
        if self.dip is None:
            return None
        return config.height * tan(radians(90 - self.dip))

    @staticmethod
    def read_from(spatial):
        """
        :type spatial: Phidgets.Devices.Spatial.Spatial
        """
        try:
            return AccelerometerFix(spatial.getAcceleration(0),
                                    spatial.getAcceleration(1),
                                    spatial.getAcceleration(2))
        except PhidgetException:
            print "WARNING: Could not read accelerometer!"
            return AccelerometerFix()

    def as_dict(self):
        return OrderedDict((
            ('a0', self.a0),
            ('a1', self.a1),
            ('a2', self.a2),
            ('dip_angle', self.dip),
            ('distance', self.dist),
            ('height', config.height)
        ))