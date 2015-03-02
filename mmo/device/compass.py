from collections import OrderedDict


class CompassFix:
    """
    Convenience for reading and presenting compass fixes
    """
    def __init__(self, c0, c1, c2):
        self.compass0 = c0
        self.compass1 = c1
        self.compass2 = c2

    @staticmethod
    def from_spatial(spatial):
        """
        :type spatial: Phidgets.Devices.Spatial.Spatial
        """
        return CompassFix(spatial.getMagneticField(0), spatial.getMagneticField(1), spatial.getMagneticField(2))

    def as_dict(self):
        return OrderedDict((
            ('compass0', self.compass0),
            ('compass1', self.compass1),
            ('compass2', self.compass2)
        ))