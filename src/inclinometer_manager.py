'''
Created on 26. nov. 2014
@author: PPAR
'''
import sys, time
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
        self.min_sampling_period_in_secs_magnetic = 0.01 # Max sampling rate for the compass is 125HZ (min sampling period is 0.008 sec)
        
        self.sampling_duration_in_secs = sampling_duration_in_secs
        
        self.accelerometer_data = {}
        self.angular_data = {}
        self.magnetic_data = {}

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
    
    def getStandardMeasurements(self):
        #Clean data
        self.accelerometer_data.clear()
        self.angular_data.clear()
        print("Cleared acceleration_data(%s) & angular_data(%s)" % (str(self.accelerometer_data), str(self.angular_data)))
        
        timestamp_str = time.strftime("%c")
        
        self.accelerometer_data["timestamp"] = timestamp_str
        self.accelerometer_data["acc_X"] = []
        self.accelerometer_data["acc_Y"] = []
        self.accelerometer_data["acc_Z"] = []
        
        self.angular_data["timestamp"] = timestamp_str
        self.angular_data["ang_X"] = []
        self.angular_data["ang_Y"] = []
        self.angular_data["ang_Z"] = []
       
        t0 = time.clock()
        time_delta = 0 
        is_time_sample_magnetic_data = 0.0
        
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
    
    def getMagneticMeasurements(self):
        #Clean data
        self.magnetic_data.clear()
        print("Cleared magnetic_data(%s)" % (str(self.magnetic_data)))
        
        sampling_period = self.min_sampling_period_in_secs_magnetic
        if(self.sampling_period_in_secs > self.min_sampling_period_in_secs_magnetic):
            sampling_period = self.sampling_period_in_secs
            
        timestamp_str = time.strftime("%c")
        
        self.magnetic_data["timestamp"] = timestamp_str
        self.magnetic_data["X"] = []
        self.magnetic_data["Y"] = []
        self.magnetic_data["Z"] = []
       
        t0 = time.clock()
        time_delta = 0 
        
        while(time_delta < self.sampling_duration_in_secs):
            mag_x = mag_y = mag_z = "N/A"
            try:
                mag_x = self.spatial.getMagneticField(0)
                mag_y = self.spatial.getMagneticField(1)
                mag_z = self.spatial.getMagneticField(2)
                
                self.magnetic_data["X"].append(mag_x)
                self.magnetic_data["Y"].append(mag_y)
                self.magnetic_data["Z"].append(mag_z)
            
            except Exception as e:
                print("mag_x: %r, mag_y= %r, mag_z= %r" %(mag_x, mag_y, mag_z))
                print("%r - PhidgetException %i when trying to close the phidget: %s" % (time_delta, e.code, e.details), file=sys.stderr)    
                
            
              
            time.sleep(sampling_period)
            time_delta = time.clock() - t0   
        
        print(">>> Get measurement - time_delta: %.4f" % (time_delta))
        return self.magnetic_data       
    

    def closeDownInclinometer(self):
        try:
            self.spatial.closePhidget()
        except PhidgetException as e:
            print("PhidgetException %i when trying to close the phidget: %s" % (e.code, e.details), file=sys.stderr)
            raise e
    