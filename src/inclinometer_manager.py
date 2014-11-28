'''
Created on 26. nov. 2014
@author: PPAR
'''
import sys, time, datetime

from ctypes import *

#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan

class InclinometerManager(object):
    
    def __init__(self, connection_timeout_in_secs, sampling_period_in_secs, sampling_duration_in_secs):
        self.connection_timeout_in_secs = connection_timeout_in_secs
        self.sampling_period_in_secs = sampling_period_in_secs
        self.sampling_duration_in_secs = sampling_duration_in_secs
        self.accelerometer_data = {}
        self.angular_data = {}


    def displayDeviceInfo(self):
        print("|------------|----------------------------------|--------------|------------|")
        print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
        print("|------------|----------------------------------|--------------|------------|")
        print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (self.spatial.isAttached(), self.spatial.getDeviceName(), self.spatial.getSerialNum(), self.spatial.getDeviceVersion()))
        print("|------------|----------------------------------|--------------|------------|")
        print("No of Acceleration Axes: %i - No of Gyro Axes: %i - No of Compass Axes: %i" % (self.spatial.getAccelerationAxisCount(), self.spatial.getGyroAxisCount(), self.spatial.getCompassAxisCount()))
        print("Data Rate: %i msec, (Min) Data Rate: %i msec, (Max) Data Rate: %i msec" % (self.spatial.getDataRate(), self.spatial.getDataRateMin(), self.spatial.getDataRateMax()))
        print("Connection Timeout: %f sec, Sampling Period: %f sec, Sampling Duration: %f sec" % (self.connection_timeout_in_secs, self.sampling_period_in_secs, self.sampling_duration_in_secs))

    
    def startUpInclinometer(self):
        # create an instance of the Spatial phidget
        try:
            self.spatial = Spatial()
        except RuntimeError as e:
            print("RuntimeError %i while creating the Phidget (Spatial) object: %s" % (e.code, e.details), file=sys.stderr)
            raise e
        
        #connect & open the phidget
        try:
            self.spatial.openPhidget()
            self.spatial.waitForAttach(self.connection_timeout_in_secs * 1000)
        except  PhidgetException as e:
            print("PhidgetException %i when attaching & opening the phidget: %s" % (e.code, e.details), file=sys.stderr)
            
            try:
                self.spatial.closePhidget()
            except PhidgetException as e:
                print("PhidgetException %i when trying to close the phidget: %s" % (e.code, e.details), file=sys.stderr)
            
            raise e
        
        else:
            self.displayDeviceInfo()
    
    def getMeasurements(self):
        #Clean data
        self.accelerometer_data.clear()
        self.angular_data.clear()
        print("Cleared acceleration_data(%s) & angular_data(%s)" % (str(self.accelerometer_data), str(self.angular_data)))
        t0 = time.clock()
        time_delta = 0
        
        timestamp_str = time.strftime("%c")
        
        self.accelerometer_data["timestamp"] = timestamp_str
        self.accelerometer_data["acc_X"] = []
        self.accelerometer_data["acc_Y"] = []
        self.accelerometer_data["acc_Z"] = []
        
        self.angular_data["timestamp"] = timestamp_str
        self.angular_data["ang_X"] = []
        self.angular_data["ang_Y"] = []
        self.angular_data["ang_Z"] = []
        
        
        while(time_delta < self.sampling_duration_in_secs):
            
            self.accelerometer_data["acc_X"].append((self.spatial.getAcceleration(0)))
            self.accelerometer_data["acc_Y"].append((self.spatial.getAcceleration(1)))
            self.accelerometer_data["acc_Z"].append((self.spatial.getAcceleration(2)))            
            
            self.angular_data["ang_X"].append(self.spatial.getAngularRate(0))
            self.angular_data["ang_Y"].append(self.spatial.getAngularRate(1))
            self.angular_data["ang_Z"].append(self.spatial.getAngularRate(2))
            
            time.sleep(self.sampling_period_in_secs)
            time_delta = time.clock() - t0   
        
        print(">>> Get measurement - time_delta: %.4f" % (time_delta))
        return self.accelerometer_data, self.angular_data       
    

    def closeDownInclinometer(self):
        try:
            self.spatial.closePhidget()
        except PhidgetException as e:
            print("PhidgetException %i when trying to close the phidget: %s" % (e.code, e.details), file=sys.stderr)
            raise e
    