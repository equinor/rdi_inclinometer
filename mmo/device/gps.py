# noinspection PyPep8Naming
# because GPS is not really a constant after all
from Phidgets.Devices.GPS import GPS as GpsPhidget
from abc import abstractmethod

from Phidgets.PhidgetException import PhidgetException

import mmo
from mmo.device.device import Device
from mmo.device.output import GpsFix


class GpsLike(Device):
    @abstractmethod
    def get_fix(self):
        pass


class Gps(GpsLike):
    def __init__(self):
        gps = GpsPhidget()
        self.gps = gps
        gps.setOnAttachHandler(self.attach_handler)
        gps.setOnDetachHandler(self.detach_handler)
        gps.setOnPositionChangeHandler(self.position_change_handler)
        gps.openPhidget()
        try:
            gps.waitForAttach(1000)
        except PhidgetException:
            mmo.logger.warn("WARNING: No GPS connected")

    def get_fix(self):
        if not self.gps.isAttached():
            mmo.logger.warn("WARNING: No GPS Attached")
            return GpsFix()

        if not self.gps.getPositionFixStatus():
            # No good GPS fix
            return GpsFix()

        return GpsFix.from_phidget(self.gps)

    def attach_handler(self, event):
        super(Gps, self).attach_handler(event)
        mmo.status.gps_connected = True

    def detach_handler(self, event):
        super(Gps, self).detach_handler(event)
        mmo.status.gps_connected = False
        mmo.logger.warn("WARNING: GPS disconnected")

    # noinspection PyUnusedLocal
    # just to show that this parameter comes from the library anyway
    def position_change_handler(self, event):
        fix = GpsFix.from_phidget(self.gps)
        mmo.status.update_position(fix)

