from Phidgets.PhidgetException import PhidgetException

from mmo import config
from mmo.device import GpsFix
from mmo.device import Gyro
from mmo.device import AccelerometerFix
from mmo.device import CompassFix
from socket import gethostname

from enum import Enum


class ButtonType(Enum):
    short = 1
    long = 2

    def __str__(self):
        return self.name

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
        self.storage = storage
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

    # Inspection disabled due to IDEA interpreting enum as int
    # noinspection PyTypeChecker
    def key_pressed(self, length):
        if length < 1.0:
            self.button_click(ButtonType.short)
        else:
            self.button_click(ButtonType.long)

    def button_click(self, button_type):
        """
        :type button_type: ButtonType
        """

        gps_fix = GpsFix.read_from(self.gps)
        accelerometer_fix = AccelerometerFix.read_from(self.spatial)
        compass_fix = CompassFix.from_spatial(self.spatial)
        self.storage.store(host_name=gethostname(),
                           gps_fix=gps_fix,
                           gyro=self.gyro,
                           accelerometer_fix=accelerometer_fix,
                           compass_fix=compass_fix,
                           typ=str(button_type))

        if button_type == ButtonType.long:
            self.reset_gyro()
            # The user should hold the binoculars still for two seconds
            self.button.beep(2.0)
        else:
            self.button.beep(0.2)

    # Updates the gyro integral
    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)

    def reset_gyro(self):
        print "Long press detected - zeroing things"
        self.spatial.zeroGyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)
        self.gyro.reset()

    @staticmethod
    def attach_handler(event):
        attached_device = event.device
        serial_number = attached_device.getSerialNum()
        device_name = attached_device.getDeviceName()
        print("Connected to Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))