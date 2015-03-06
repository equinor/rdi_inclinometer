from abc import abstractmethod

from Phidgets.Devices.Spatial import Spatial as SpatialPhidget

import mmo
from mmo.device.device import Device
from mmo.device import Gyro
from mmo.device.output import AccelerometerFix, CompassFix, RollPitchYaw


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

    @abstractmethod
    def get_gravity_raw(self):
        """
        :returns: (float, float, float)
        """
        pass

    def get_gravity(self):
        """
        Gravity, rotated to account for rotated spatial device
        :returns: (float, float, float)
        """
        return mmo.config.axis_translator.translate(*self.get_gravity_raw())

    def get_compass(self):
        return mmo.config.axis_translator.translate(*self.get_compass_raw())

    @abstractmethod
    def get_compass_raw(self):
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

    def get_gravity_raw(self):
        """
        :returns: (float, float, float)
        """
        return (self.spatial.getAcceleration(0),
                self.spatial.getAcceleration(1),
                self.spatial.getAcceleration(2))

    def get_compass_raw(self):
        return (self.spatial.getMagneticField(0),
                self.spatial.getMagneticField(1),
                self.spatial.getMagneticField(2))

    def get_accelerometer_fix(self):
        if not self.spatial.isAttached():
            return AccelerometerFix()
        return AccelerometerFix(*self.get_gravity_raw())

    def get_roll_pitch_yaw(self):
        return RollPitchYaw.calculate_from(gravity=self.get_gravity(), magnetic_fields=self.get_compass())

    def get_compass_fix(self):
        if not self.spatial.isAttached():
            return CompassFix()
        return CompassFix(*self.get_compass_raw())

    def get_gyro(self):
        return self.gyro

    def reset_gyro(self):
        print "Resetting gyro"
        self.spatial.zeroGyro()
        self.gyro.reset()

    i = 0
    # Updates the gyro integral
    # noinspection PyUnusedLocal
    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)

    def attach_handler(self, event):
        super(Spatial, self).attach_handler(event)
        mmo.status.spatial_connected = True
        self.spatial.setDataRate(mmo.config.get_sampling_rate())
        self.reset_gyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)

    def detach_handler(self, event):
        super(Spatial, self).detach_handler(event)
        mmo.status.spatial_connected = False
        print "WARNING: Spatial disconnected"


