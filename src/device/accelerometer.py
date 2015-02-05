from config import config
from collections import OrderedDict
from math import acos, pi, radians, tan

class AccelerometerFix:
    def __init__(self, a0, a1, a2):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.dip = self.dip_angle()
        self.dist = self.distance()

    def __str__(self):
        return "a0={}, a1={}, a2={}, dip={}".format(self.a0, self.a1, self.a2, self.dip_angle())

    def dip_angle(self):
        # l = sqrt(self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2)
        r1 = acos(self.a1)

        dip1 = 90 - (r1 * 180 / pi)
        return dip1

    def distance(self):
        return config.height * tan(radians(90 - self.dip))

    @staticmethod
    def read_from(spatial):
        """
        :type spatial: Spatial
        """
        return AccelerometerFix(spatial.getAcceleration(0),
                                spatial.getAcceleration(1),
                                spatial.getAcceleration(2))

    def as_dict(self):
        return OrderedDict((
            ('a0', self.a0),
            ('a1', self.a1),
            ('a2', self.a2),
            ('dip_angle', self.dip),
            ('distance', self.dist),
            ('height', config.height)
        ))