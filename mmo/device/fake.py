from datetime import datetime
from mmo.device import CompassFix, AccelerometerFix, Gyro
from mmo.device.gps import GpsLike, GpsFix
from mmo.device.spatial import SpatialLike


class FakeGps(GpsLike):
    def get_fix(self):
        return GpsFix(timestamp=datetime.now(),
                      latitude=13,
                      longitude=37,
                      altitude=20,
                      heading=60,
                      velocity=5)


class FakeSpatial(SpatialLike):
    def reset_gyro(self):
        print "Fakely resetting gyro"

    def get_compass_fix(self):
        return CompassFix()

    def get_gyro(self):
        return Gyro(0.0, 60.0, 0.0)

    def get_accelerometer_fix(self):
        return AccelerometerFix()

