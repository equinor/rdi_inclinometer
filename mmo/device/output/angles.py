from collections import OrderedDict
from math import atan2, atan, sin, cos, degrees


class RollPitchYaw(object):
    def __init__(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    @staticmethod
    def calculate_from(gravity, magnetic_fields):
        print("RollPitchYaw:")
        print("    gravity -> {}".format(gravity))
        print("    magnetic_fields -> {}".format(magnetic_fields))
        g0, g1, g2 = gravity
        c0, c1, c2 = magnetic_fields

        if g0 is None or c0 is None:
            return RollPitchYaw(None, None, None)

        roll_angle_rad = atan2(-g0, g2)
        pitch_angle_rad = atan(-g1 / ((-g0 * sin(roll_angle_rad)) + (g2 * cos(roll_angle_rad))))
        yaw_angle_rad = atan2(
            (c2 * sin(roll_angle_rad))
            - (-c0 * cos(roll_angle_rad))
            ,
            (c1 * cos(pitch_angle_rad))
            + (-c0 * sin(pitch_angle_rad) * sin(roll_angle_rad))
            + (c2 * sin(pitch_angle_rad) * cos(roll_angle_rad)))

        roll = degrees(roll_angle_rad)
        pitch = degrees(pitch_angle_rad)
        yaw = (degrees(yaw_angle_rad) + 360) % 360
        return RollPitchYaw(roll=round(roll, 2), pitch=round(pitch, 2), yaw=round(yaw, 2))

    def as_dict(self):
        return OrderedDict((
            ("roll", self.roll),
            ("pitch", self.pitch),
            ("yaw", self.yaw))
        )

    def __str__(self):
        return "roll={}, pitch={}, yaw={}".format(self.roll, self.pitch, self.yaw)
