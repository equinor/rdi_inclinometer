from collections import OrderedDict
from Phidgets.PhidgetException import PhidgetException


class CompassFix:
    """
    Convenience for reading and presenting compass fixes
    """
    def __init__(self, c0=None, c1=None, c2=None):
        self.compass0 = c0
        self.compass1 = c1
        self.compass2 = c2

    @staticmethod
    def from_spatial(spatial):
        """
        :type spatial: Phidgets.Devices.Spatial.Spatial
        """
        try:
            return CompassFix(spatial.getMagneticField(0), spatial.getMagneticField(1), spatial.getMagneticField(2))
        except PhidgetException:
            print "WARNING: Could not get Compass fix"
            return CompassFix()

    def as_dict(self):
        return OrderedDict((
            ('compass0', self.compass0),
            ('compass1', self.compass1),
            ('compass2', self.compass2)
        ))