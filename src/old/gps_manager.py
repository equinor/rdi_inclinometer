
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS


class GPSManager(object):

    def __init__(self, connection_timeout_in_secs, sampling_period_in_secs, sampling_duration_in_secs):
        self.connection_timeout_in_secs = connection_timeout_in_secs

        self.sampling_period_in_secs = sampling_period_in_secs
        self.min_sampling_period_in_secs_magnetic = 0.01 # Max sampling rate for the compass is 125HZ (min sampling period is 0.008 sec)

        self.sampling_duration_in_secs = sampling_duration_in_secs


    def displayDeviceInfo(self):
        print("|------------|----------------------------------|--------------|------------|")
        print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
        print("|------------|----------------------------------|--------------|------------|")
        print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (self.GPS.isAttached(), self.GPS.getDeviceName(), self.GPS.getSerialNum(), self.GPS.getDeviceVersion()))
        print("|------------|----------------------------------|--------------|------------|")
        try:
            print("GPS %i: Latitude: %F, Longitude: %F, Altitude: %F, Date: %s, Time: %s" % (self.GPS.getSerialNum(), self.GPS.getLatitude(), self.GPS.getLongitude(), self.GPS.getAltitude(), self.GPS.getDate().toString(), self.GPS.getTime().toString()))
        except PhidgetException as e:
            print("PhidgetException (%i) when attaching & opening the phidget: %s" % (e.code, e.details))
        raise e

    def startUpGPS(self):
        # create an instance of the GPS phidget
        try:
            self.GPS = GPS()
        except RuntimeError as e:
            print("RuntimeError (%i) while creating the Phidget (GPS) object: %s" % (e.code, e.details))
            raise e

        #connect & open the phidget
        try:
            self.GPS.openPhidget()
            self.GPS.waitForAttach(self.connection_timeout_in_secs * 1000)
        except  PhidgetException as e:
            print("PhidgetException (%i) when attaching & opening the phidget: %s" % (e.code, e.details))

            try:
                self.GPS.closePhidget()
            except PhidgetException as e:
                print("PhidgetException (%i) when trying to close the phidget: %s" % (e.code, e.details))

            raise e

        else:
            self.displayDeviceInfo()


    def closeDownGPS(self):
        try:
            self.GPS.closePhidget()
        except PhidgetException as e:
            print("PhidgetException %i when trying to close the phidget: %s" % (e.code, e.details))
            raise e