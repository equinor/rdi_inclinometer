from Phidgets.PhidgetException import PhidgetException

from mmo.config import config
from mmo.device import GpsFix
from mmo.device import Gyro
from mmo.device import AccelerometerFix
from mmo.device import CompassFix


class Binoculars:
    """
    Sews together all the sensors for the binocular

    Sample rate cannot be shorter than 8ms, or the compass won't work

    """
    def __init__(self,
                 button,
                 gps,
                 spatial,
                 storage):
        self.store = storage
        self.gyro = Gyro()
        self.button = button
        button.key_pressed = self.key_pressed

        if gps:
            self.gps = gps
            gps.setOnAttachHandler(self.attach_handler)
            try:
                gps.openPhidget()
                gps.waitForAttach(1000)
            except PhidgetException:
                print "Could not connect to GPS"
                raise

        if spatial:
            self.spatial = spatial
            spatial.setOnAttachHandler(self.attach_handler)
            spatial.openPhidget()
            spatial.waitForAttach(1000)
            spatial.setDataRate(config.sampling_rate)

    def key_pressed(self, length):
        if length < 1.0:
            self.key_pressed_short()
        else:
            self.key_pressed_long()

    def key_pressed_short(self):
        gps_fix = GpsFix.read_from(self.gps)
        accelerometer_fix = AccelerometerFix.read_from(self.spatial)
        compass_fix = CompassFix.from_spatial(self.spatial)
        self.store.store(gps_fix, self.gyro, accelerometer_fix, compass_fix, typ="Short_press")

    def key_pressed_long(self):
        print "Long press detected - zeroing things"
        self.spatial.zeroGyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)
        self.gyro.reset()
        accelerometer_fix = AccelerometerFix.read_from(self.spatial)
        gps_fix = GpsFix.read_from(self.gps)
        compass_fix = CompassFix.from_spatial(self.spatial)
        self.store.store(gps_fix, self.gyro, accelerometer_fix, compass_fix, typ="Long_press")

    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)

    @staticmethod
    def attach_handler(event):
        attached_device = event.device
        serial_number = attached_device.getSerialNum()
        device_name = attached_device.getDeviceName()
        print("Connected to Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))