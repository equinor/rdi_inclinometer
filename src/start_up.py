'''
Created on 26. nov. 2014
@author: PPAR
'''

import inclinometer_manager, output_manager, gps_manager
from Phidgets import PhidgetException

try:
    im = inclinometer_manager.InclinometerManager(5, 0.005, 0.5)
    gps = gps_manager.GPSManager(5, 0.005, 0.5)
except RuntimeError as e:
    print("Error (%i) while creating the Phidget object: %s" % (e.code, e.details))
    print("Exiting ...")
    exit(1)

try:
    im.startUpInclinometer()
    print("Inclinometer STARTED-UP.....")
    #gps.startUpGPS()
    print("GPS STARTED-UP.....")
except PhidgetException as e:
    print("Phidget Exception (%i) when trying to STARTUP the Phidget: %s" % (e.code, e.details))
    exit(1)

om = output_manager.OutputManager()

continueLoop = True
while continueLoop:
    data_type = raw_input("(h) - horizon, (m) - measurement, (q) quit> ")
    
    if data_type == "q":
        break
    
    if data_type == "h" or data_type == "m":
        
        readable_data_type = "measurement"
        if(data_type == "h"):
            readable_data_type = "horizon"
            
        acc_data, ang_data, mag_data = im.getMeasurements()
        om.saveData(acc_data, ang_data, mag_data, readable_data_type)


try:
    im.closeDownInclinometer()
    print("Inclinometer CLOSED-DOWN.....")
    #gps.closeDownGPS()
    print("GPS CLOSED-DOWN.....")
except PhidgetException as e:
    print("Phidget Exception (%i) when trying to CLOSEDOWN the inclinometer: %s" % (e.code, e.details))
    exit(1)

exit(0)