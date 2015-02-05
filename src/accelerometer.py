from math import sqrt, acos, pi, radians, tan
from config import height

class AccelerometerFix:
    def __init__(self, a0, a1, a2):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.dip_angle()

    def __str__(self):
        return "a0={}, a1={}, a2={}, dip={}".format(self.a0, self.a1, self.a2, self.dip_angle())

    def dip_angle(self):
        l = sqrt(self.a0 * self.a0 + self.a1 * self.a1 + self.a2 * self.a2)
        print "l={}".format(l)
        r1 = acos(self.a1)

        dip1 = 90 - (r1 * 180 / pi)
        return dip1

    def distance(self):
        height * tan(radians(90 - self.dip_angle()))

    @staticmethod
    def read_from(spatial):
        """

        :type spatial: Spatial
        """
        return AccelerometerFix(spatial.getAcceleration(0),
                                spatial.getAcceleration(1),
                                spatial.getAcceleration(2))

    def to_csv(self):
        return "{};{};{};{};{};{};".format(self.a0, self.a1, self.a2, self.dip_angle(), self.distance(), height)

    @staticmethod
    def csv_headers():
        return "Accelerometer_0;Accelerometer_1;Accelerometer_2;Dip_angle;Distance;Height"