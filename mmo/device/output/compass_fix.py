from collections import OrderedDict


class CompassFix(object):
    """
    Convenience for reading and presenting compass fixes
    """

    def __init__(self, c0=None, c1=None, c2=None):
        self.compass0 = c0
        self.compass1 = c1
        self.compass2 = c2

    def as_dict(self):
        return OrderedDict((
            ('c0', self.compass0),
            ('c1', self.compass1),
            ('c2', self.compass2)
        ))

    def __str__(self):
        return "c0={}, c1={}, c2={}".format(self.compass0, self.compass1, self.compass2)