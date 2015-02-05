class CompassFix:
    """
    Convenience for reading and presenting compass fixes
    """
    def __init__(self, c0, c1, c2):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2

    def to_csv(self):
        return "{};{};{};".format(self.c0, self.c1, self.c2)

    @staticmethod
    def from_spatial(spatial):
        """
        :type spatial: Phidgets.Devices.Spatial.Spatial
        """
        return CompassFix(spatial.getMagneticField(0), spatial.getMagneticField(1), spatial.getMagneticField(2))

    @staticmethod
    def csv_headers():
        return "Compass_0;Compass_1;Compass_2;"
