from collections import OrderedDict
# from Phidgets.Devices.Spatial import Spatial as SpatialPhidget


class Gyro(object):
    def __init__(self, gyro0=0.0, gyro1=0.0, gyro2=0.0):
        self.gyro0 = gyro0
        self.gyro1 = gyro1
        self.gyro2 = gyro2

    _fields = ('gyro0', 'gyro1', 'gyro2')

    def add(self, dd0, dd1, dd2, scaling_factor=1.0):
        self.gyro0 += dd0 * scaling_factor
        self.gyro1 += dd1 * scaling_factor
        self.gyro2 += dd2 * scaling_factor

    def reset(self):
        self.gyro0 = 0.0
        self.gyro1 = 0.0
        self.gyro2 = 0.0

    def as_dict(self):
        return OrderedDict((
            ('gyro0', self.gyro0),
            ('gyro1', self.gyro1),
            ('gyro2', self.gyro2)
        ))

    def __str__(self):
        return "Gyro(pitch={0}, roll={1}, yaw={2})".format(self.gyro0, self.gyro1, self.gyro2)

    def update_from(self, spatial):
        """
        :type spatial: SpatialPhidget
        """
        self.add(spatial.getAngularRate(0),
                 spatial.getAngularRate(1),
                 spatial.getAngularRate(2),
                 spatial.getDataRate() / 1000.0)
