from collections import OrderedDict, deque
# from Phidgets.Devices.Spatial import Spatial as SpatialPhidget


class Gyro(object):
    samplePitch = deque([], 5)
    sampleRoll = deque([], 5)
    sampleYaw = deque([], 5)

    def __init__(self, gyro0=0.0, gyro1=0.0, gyro2=0.0):
        self.gyro0 = gyro0
        self.samplePitch.append(gyro0)

        self.gyro1 = gyro1
        self.sampleRoll.append(gyro1)

        self.gyro2 = gyro2
        self.sampleYaw.append(gyro2)

    _fields = ('gyro0', 'gyro1', 'gyro2')

    def add(self, dd0, dd1, dd2, scaling_factor=1.0):
        self.samplePitch.append(dd0)
        self.sampleRoll.append(dd1)
        self.sampleYaw.append(dd2)

        self.gyro0 += dd0 * scaling_factor
        self.gyro1 += dd1 * scaling_factor
        self.gyro2 += dd2 * scaling_factor

    def reset(self):
        self.gyro0 = 0.0
        self.samplePitch.clear()

        self.gyro1 = 0.0
        self.sampleRoll.clear()

        self.gyro2 = 0.0
        self.sampleYaw.clear()

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
        :type spatial: SpatialPhidget or tuple
        """
        if isinstance(spatial, list):
            self.add(spatial[0],
                     spatial[1],
                     spatial[2],
                     spatial[3] / 1000.0)
        else:
            self.add(spatial.getAngularRate(0),
                     spatial.getAngularRate(1),
                     spatial.getAngularRate(2),
                     spatial.getDataRate() / 1000.0)

    @staticmethod
    def average(iterable):
        return reduce(lambda x, y: x + y, iterable) / len(iterable)

    def get_avg_pitch(self):
        return Gyro.average(self.samplePitch)

    def get_avg_roll(self):
        return Gyro.average(self.sampleRoll)

    def get_avg_yaw(self):
        return Gyro.average(self.sampleYaw)

    def __getitem__(self, index):
        if index == 0:
            return self.gyro0
        elif index == 1:
            return self.gyro1
        elif index == 2:
            return self.gyro2
        else:
            raise IndexError("Gyro has only 3 items")
