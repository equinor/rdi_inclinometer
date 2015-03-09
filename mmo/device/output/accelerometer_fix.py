from collections import OrderedDict


class AccelerometerFix:
    def __init__(self, a0=None, a1=None, a2=None):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2

    def __str__(self):
        return "a0={}, a1={}, a2={}".format(self.a0, self.a1, self.a2)

    def as_dict(self):
        return OrderedDict((
            ('a0', self.a0),
            ('a1', self.a1),
            ('a2', self.a2)
        ))