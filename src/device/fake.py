class FakePhidget:
    def setOnAttachHandler(self, attach_handler):
        pass

    def openPhidget(self, serial=-1):
        pass

    def waitForAttach(self, timeout):
        pass

class FakeGps(FakePhidget):
    def getDate(self):
        class FakeDate:
            year=2014
            month=1
            day=1
        return FakeDate()

    def getTime(self):
        class FakeTime:
            hour=13
            min=00
            sec=30
            ms=500
        return FakeTime()

    def getAltitude(self):
        return 20.0

    def getLatitude(self):
        return 13.0

    def getPositionFixStatus(self):
        return True

    def getVelocity(self):
        return 1.0

    def getLongitude(self):
        return 37.0

    def getHeading(self):
        return 60.0


class FakeSpatial(FakePhidget):


    def setOnAttachHandler(self, attachHandler):
        pass

    def setDataRate(self, value):
        pass

    def getDataRate(self):
        return 8

    def getAngularRate(self, index):
        return 0.1

    def zeroGyro(self):
        pass

    def getMagneticField(self, index):
        return 0.2

    def getAcceleration(self, index):
        return 0.5

    def setOnSpatialDataHandler(self, on_spatial_data_handler):
        pass