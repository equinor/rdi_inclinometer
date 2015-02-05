from Phidgets.Devices.Spatial import Spatial


class Gyro:
    def __init__(self):
        self.d0 = 0.0
        self.d1 = 0.0
        self.d2 = 0.0

    def add(self, dd0, dd1, dd2, scaling_factor=1.0):
        self.d0 += dd0 * scaling_factor
        self.d1 += dd1 * scaling_factor
        self.d2 += dd2 * scaling_factor

    def reset(self):
        self.d0 = 0.0
        self.d1 = 0.0
        self.d2 = 0.0

    def __str__(self):
        return "{} {} {}".format(self.d0, self.d1, self.d2)

    def to_csv(self):
        return "{};{};{};".format(self.d0, self.d1, self.d2)

    def update_from(self, spatial):
        """
        :type spatial: Spatial
        """
        self.add(spatial.getAngularRate(0),
                 spatial.getAngularRate(1),
                 spatial.getAngularRate(2),
                 spatial.getDataRate() / 1000.0)

    @staticmethod
    def csv_headers():
        return "Gyro_0;Gyro_1;Gyro_2;"
