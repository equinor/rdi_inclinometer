from abc import abstractmethod

from Phidgets.Devices.Spatial import Spatial as SpatialPhidget

from mmo.device.device import Device

from mmo import config

from mmo.device import AccelerometerFix, CompassFix, Gyro


class SpatialLike(Device):
    @abstractmethod
    def get_accelerometer_fix(self):
        pass

    @abstractmethod
    def get_compass_fix(self):
        pass

    @abstractmethod
    def reset_gyro(self):
        pass

    @abstractmethod
    def get_gyro(self):
        pass


class Spatial(SpatialLike):
    """
    Sample rate cannot be shorter than 8ms, or the compass won't work
    """

    def __init__(self):
        spatial = SpatialPhidget()
        self.spatial = spatial
        self.gyro = Gyro()
        spatial.setOnAttachHandler(self.attach_handler)
        spatial.setOnDetachHandler(self.detach_handler)
        spatial.openPhidget()

    def get_accelerometer_fix(self):
        if not self.spatial.isAttached():
            return AccelerometerFix()
        return AccelerometerFix.read_from(self.spatial)

    def get_compass_fix(self):
        if not self.spatial.isAttached():
            return CompassFix()
        return CompassFix.from_spatial(self.spatial)

    def get_gyro(self):
        return self.gyro

    def reset_gyro(self):
        print "Resetting gyro"
        self.spatial.zeroGyro()
        self.gyro.reset()

    # Updates the gyro integral
    # noinspection PyUnusedLocal
    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)

    def attach_handler(self, event):
        super(Spatial, self).attach_handler(event)
        self.spatial.setDataRate(config.sampling_rate)
        self.reset_gyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)

    def detach_handler(self, event):
        super(Spatial, self).detach_handler(event)
        print "WARNING: Spatial disconnected"


