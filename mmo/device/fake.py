from datetime import datetime
import mmo
from mmo.device.gyro import Gyro
from mmo.device.output import CompassFix, AccelerometerFix, RollPitchYaw
from mmo.device.gps import GpsLike, GpsFix
from mmo.device.spatial import SpatialLike
from mmo import status
import threading
import time
from collections import namedtuple
from random import uniform

SpatialEventData = namedtuple('SpatialEventData',
                              'data, numAccelAxes, numGyroAxes, numCompassAxes dataRate')


class FakeGps(GpsLike):
    def __init__(self):
        status.gps_connected = True

    def get_fix(self):
        return GpsFix(timestamp=datetime.utcnow(),
                      latitude=13,
                      longitude=37,
                      altitude=20,
                      heading=60,
                      velocity=5)


class FakeSpatialDevice(object):
    def __init__(self):
        self._event_handler = None
        self._attach_handler = None
        self._detach_handler = None
        self.lock = threading.Lock()
        self._attached = False
        self._running = False

    def _run(self):
        while True:
            self.lock.acquire()
            try:
                if not self._running:
                    break
                if self._attached:
                    data = [
                           [uniform(0.0, 0.3), uniform(0.1, 0.5), uniform(0.4, 0.8)],  # accelerator
                           [uniform(0.8, 1.0), uniform(0.4, 0.8), uniform(0.1, 0.2)],  # gyro
                           [2.0, 2.0, 0.4]    # compass
                    ]
                    spatialEvent = SpatialEventData(data, 3, 3, 3, 200)

                    if self._event_handler:
                        self._event_handler(spatialEvent)
                    else:
                        self._attach_handler({'attached': True})
            finally:
                self.lock.release()

            time.sleep(1)

    def setOnAttachHandler(self, handler):
        self._attach_handler = handler
        self._attached = True

    def setOnDetachHandler(self, handler):
        self._detach_handler = handler

    def setOnSpatialDataHandler(self, handler):
        self._event_handler = handler

    def run(self):
        self._running = True
        thread = threading.Thread(target=self._run)

        def close_running_threads():
            self.stop()
            thread.join()

        import atexit
        # Register the function to be called on exit
        atexit.register(close_running_threads)

        import signal
        signal.signal(signal.SIGINT, close_running_threads)

        thread.start()

    def stop(self):
        self.lock.acquire()
        if self._detach_handler:
            self._detach_handler({'attached': False})
        self._running = False
        self.lock.release()


class FakeSpatial(SpatialLike):
    def __init__(self):
        status.spatial_connected = True
        self.spatial = FakeSpatialDevice()
        self.spatial.setOnAttachHandler(self.attach_handler)
        self.spatial.setOnDetachHandler(self.detach_handler)
        self.spatial.run()

        self.acceleration = None
        self.gyro = Gyro()
        self.magneticFields = None

    def get_gravity_raw(self):
        # acceleration = (0.0, 0.0, -1.0)
        print("gravity_raw: {}".format(self.acceleration))
        return self.acceleration

    def get_compass_raw(self):
        # magneticFields = (0.6, 0.6, 0.0)
        print("compas_raw: {}".format(self.magneticFields))
        return self.magneticFields

    def reset_gyro(self):
        print "Fakely resetting gyro"

    def get_compass_fix(self):
        return CompassFix(self.get_compass_raw())

    def get_gyro(self):
        fake_g = Gyro(0.0, 1.0, 0.8)
        print("Fake gyro: {}".format(fake_g))
        return fake_g

    def get_gyro_momentary(self):
        return {'gm0': 0.0,
                'gm1': 1.0,
                'gm2': 2.0}

    def get_accelerometer_fix(self):
        return AccelerometerFix(self.get_gravity_raw())

    def set_average_count(self, count):
        pass

    def update_from_config(self):
        print("Config update request")

    def get_roll_pitch_yaw(self):
        return RollPitchYaw.calculate_from(self.get_gravity_raw(), self.get_compass_raw())

    def on_spatial_data_handler(self, event):
        print("got fake spatial event: {}".format(event))
        self.acceleration = event.data[0]
        self.gyro = Gyro(*event.data[1])
        self.magneticFields = event.data[2]

    def attach_handler(self, event):
        # super(FakeSpatial, self).attach_handler(event)
        mmo.status.spatial_connected = True
        print("attach handler event")
        self.spatial.setOnSpatialDataHandler(self.on_spatial_data_handler)

    def detach_handler(self, event):
        # super(FakeSpatial, self).detach_handler(event)
        mmo.status.spatial_connected = False
        print("detach handler event")

    def stop(self):
        self.spatial.stop()
