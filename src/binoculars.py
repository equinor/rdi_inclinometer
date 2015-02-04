from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS
from Phidgets.Devices.Spatial import Spatial
from gps import GpsFix
from gyro import Gyro

class Binoculars:
    """
    Sews together all the sensors for the binocular
    """
    def __init__(self,
                 button,
                 gps=GPS(),
                 spatial=Spatial()):
        self.gyro = Gyro()
        self.button = button
        button.key_pressed = self.key_pressed

        if gps:
            self.gps = gps
            gps.setOnAttachHandler(self.attach_handler)
            try:
                gps.openPhidget()
                gps.waitForAttach(1000)
            except PhidgetException as p:
                print "Could not connect to GPS"
                raise

        if spatial:
            self.spatial = spatial
            spatial.setOnAttachHandler(self.attach_handler)
            spatial.openPhidget()
            spatial.waitForAttach(1000)
            spatial.setDataRate(spatial.getDataRateMax())

    def key_pressed(self, length):
        if length < 1.0:
            self.key_pressed_short()
        else:
            self.key_pressed_long()

    def key_pressed_short(self):
        gps_fix = GpsFix.read_from(self.gps)
        print "GPS: " + str(gps_fix)
        print "Gyro: " + str(self.gyro)

    def key_pressed_long(self):
        print "Long press detected - zeroing things"
        self.spatial.zeroGyro()
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)
        self.gyro.reset()

    def on_spatial_data_handler(self, event):
        self.gyro.update_from(self.spatial)

    @staticmethod
    def attach_handler(event):
        attached_device = event.device
        serial_number = attached_device.getSerialNum()
        device_name = attached_device.getDeviceName()
        print("Connected to Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))