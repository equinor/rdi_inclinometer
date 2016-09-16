
from datetime import datetime
from mmo.device.gyro import Gyro
from mmo.device.output import CompassFix, AccelerometerFix, RollPitchYaw
from mmo.device.gps import GpsLike, GpsFix
from mmo.device.spatial import SpatialLike
from mmo import status


class FakeGps(GpsLike):
    def __init__(self):
        status.gps_connected = True

    def get_fix(self):
        return GpsFix(timestamp=datetime.utcnow(),
                      latitude=13,
                      longitude=37,
                      altitude=20,
                      heading=60,
                      velocity=5)


class FakeSpatial(SpatialLike):
    def __init__(self):
        status.spatial_connected = True

    def get_gravity_raw(self):
        tmp = (0.0, 0.0, -1.0)
        print("gravity_raw: {}".format(tmp))
        print tmp

    def get_compass_raw(self):
        tmp = (0.6, 0.6, 0.0)
        print("compas_raw: {}".format(tmp))
        return tmp

    def reset_gyro(self):
        print "Fakely resetting gyro"

    def get_compass_fix(self):
        return CompassFix(self.get_compass_raw())

    def get_gyro(self):
        fake_g = Gyro(0.0, 1.0, 0.8)
        print("Fake gyro: {}".format(fake_g))
        return fake_g

    def get_gyro_momentary(self):
        return {'gm0': 0.0,
                'gm1': 1.0,
                'gm2': 2.0}

    def get_accelerometer_fix(self):
        return AccelerometerFix(self.get_gravity_raw())

    def set_average_count(self, count):
        pass

    def update_from_config(self):
        pass

    def get_roll_pitch_yaw(self):
        return RollPitchYaw.calculate_from(self.get_gravity_raw(), self.get_compass_raw())
