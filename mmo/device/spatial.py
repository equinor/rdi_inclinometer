from __future__ import absolute_import
from __future__ import print_function
from abc import abstractmethod

import mmo
from mmo.device.device import Device
from mmo.device.gyro import Gyro
from mmo.device.output import AccelerometerFix, CompassFix, RollPitchYaw

class SpatialLike(Device):
    @abstractmethod
    def set_average_count(self, count):
        pass

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
    def get_gyro_momentary(self):
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

    def set_sampling_rate(self, sampling_rate):
        pass

    @abstractmethod
    def update_from_config(self):
        """
        Updates the spatial device with new parameters
        :returns: None
        """
        pass


class Spatial(SpatialLike):

    """
    Sample rate cannot be shorter than 8ms, or the compass won't work
    """

    gyro = Gyro()
    spatial = None
    # averaging_array0 = [0.0]
    # averaging_array1 = [0.0]
    # averaging_array2 = [0.0]
    # averaging_index = 0
    # averaging_n = 1

    def __init__(self):
        from Phidgets.Devices.Spatial import Spatial as SpatialPhidget
        self.spatial = SpatialPhidget()
        spatial = self.spatial
        spatial.setOnAttachHandler(self.attach_handler)
        spatial.setOnDetachHandler(self.detach_handler)
        spatial.openPhidget()

    # def set_average_count(self, count):
    #     self.averaging_array0 = [0.0] * count
    #     self.averaging_array1 = [0.0] * count
    #     self.averaging_array2 = [0.0] * count
    #     self.averaging_n = count
    #     self.averaging_index = 0

    # def get_gravity_avg(self):
    #     return (sum(self.averaging_array0) / self.averaging_n,
    #             sum(self.averaging_array1) / self.averaging_n,
    #             sum(self.averaging_array2) / self.averaging_n)

    def get_gravity_raw(self):
        """
        :returns: (float, float, float)
        """
        if not self.spatial.isAttached():
            return None, None, None

        tmp = (self.spatial.getAcceleration(0),
               self.spatial.getAcceleration(1),
               self.spatial.getAcceleration(2))
        print("gravity raw: {}".format(tmp))
        return tmp

    def get_compass_raw(self):
        if not self.spatial.isAttached():
            return None, None, None
        tmp = (self.spatial.getMagneticField(0),
               self.spatial.getMagneticField(1),
               self.spatial.getMagneticField(2))
        print("compass_raw: {}".format(tmp))
        return tmp

    def get_accelerometer_fix(self):
        if not self.spatial.isAttached():
            return AccelerometerFix()
        return AccelerometerFix(*self.get_gravity_raw())

    def get_roll_pitch_yaw(self):
        rpy = RollPitchYaw.calculate_from(gravity=self.get_gravity(), magnetic_fields=self.get_compass())
        return rpy

    def get_compass_fix(self):
        if not self.spatial.isAttached():
            return CompassFix()
        return CompassFix(*self.get_compass_raw())

    def get_gyro(self):
        print("get_gyro() -> %s" % self.gyro)
        return self.gyro

    def get_gyro_momentary(self):
        gyro_momentary = {
            'gm0': self.spatial.getAngularRate(0),
            'gm1': self.spatial.getAngularRate(1),
            'gm2': self.spatial.getAngularRate(2)
        }
        return gyro_momentary

    def reset_gyro(self):
        print("reset gyro")
        self.spatial.zeroGyro()
        self.gyro.reset()

    # Updates the gyro integral
    # noinspection PyUnusedLocal
    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)
        #print("updated gyro: {}".format(self.gyro))
        spatialEventData = event.spatialData[0]
        print("spatial event: \n\taccel: {}\n\tangularRate: {}\n\tmagneticField: {}".format(spatialEventData.Acceleration, spatialEventData.AngularRate, spatialEventData.MagneticField))
        # idx = self.averaging_index
        # a0, a1, a2 = self.get_gravity()
        # self.averaging_array0[idx] = a0
        # self.averaging_array1[idx] = a1
        # self.averaging_array2[idx] = a2
        # self.averaging_index = (idx + 1) % self.averaging_n

    def attach_handler(self, event):
        super(Spatial, self).attach_handler(event)
        mmo.status.spatial_connected = True
        self.spatial.setDataRate(mmo.config.sampling_rate)
        self.reset_gyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)

    def detach_handler(self, event):
        super(Spatial, self).detach_handler(event)
        mmo.status.spatial_connected = False
        print("WARNING: Spatial disconnected")

    def update_from_config(self):
        if self.spatial.isAttached():
            self.spatial.setDataRate(mmo.config.sampling_rate)
            # self.set_average_count(mmo.config.average_sample_count)


if __name__ == "__main__":
    # Quick testing of the Spatil sensors
    s = Spatial()
    import time
    count = 10
    while count:
        count -= 1
        time.sleep(1)
