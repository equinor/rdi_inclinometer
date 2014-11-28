'''
Created on 26. nov. 2014
@author: PPAR
'''

import sys
import inclinometer_manager, output_manager
from Phidgets import PhidgetException

try:
    im = inclinometer_manager.InclinometerManager(5, 0.004, 0.5)
except RuntimeError as e:
    print("Error %i while creating the Phidget object: %s" % (e.code, e.details), file=sys.stderr)
    print("Exiting ...")
    exit(1)

try:
    im.startUpInclinometer()
    print("Inclinometer STARTED-UP.....")
except PhidgetException as e:
    print("Phidget Exception %i when trying to STARTUP the inclinometer: %s" % (e.code, e.details), file=sys.stderr)
    exit(1)

om = output_manager.OutputManager()

continueLoop = True
while continueLoop:
    action = input("(m) - measure; otherwise quit> ")
    if(action != "m"):
        continueLoop = False
    else:
        acc_data, ang_data = im.getMeasurements()
        om.saveData(acc_data, ang_data)


om.closeOutputFiles()

try:
    im.closeDownInclinometer()
    print("Inclinometer CLOSED-DOWN.....")
except PhidgetException as e:
    print("Phidget Exception %i when trying to CLOSEDOWN the inclinometer: %s" % (e.code, e.details), file=sys.stderr)
    exit(1)

exit(0)