from datetime import datetime
from mmo.device import Gyro
from mmo.device.output import CompassFix, AccelerometerFix
from mmo.device.gps import GpsLike, GpsFix
from mmo.device.spatial import SpatialLike


class FakeGps(GpsLike):
    def get_fix(self):
        return GpsFix(timestamp=datetime.utcnow(),
                      latitude=13,
                      longitude=37,
                      altitude=20,
                      heading=60,
                      velocity=5)


class FakeSpatial(SpatialLike):
    def get_gravity_raw(self):
        return 0.0, 0.0, -1.0

    def get_compass_raw(self):
        return 0.6, 0.6, 0.0

    def reset_gyro(self):
        print "Fakely resetting gyro"

    def get_compass_fix(self):
        return CompassFix(*self.get_compass_raw())

    def get_gyro(self):
        return Gyro(0.0, 60.0, 0.0)

    def get_accelerometer_fix(self):
        return AccelerometerFix(*self.get_gravity_raw())

    def set_average_count(self, count):
        pass