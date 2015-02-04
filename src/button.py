from Phidgets.Devices.InterfaceKit import InterfaceKit

def inputChanged(event):
    print("Sensor: {} {}".format(event.index, event.state))

def handleAttach(event):
    attachedDevice = event.device
    serialNumber = attachedDevice.getSerialNum()
    deviceName = attachedDevice.getDeviceName()
    print("Hello to Device " + str(deviceName) + ", Serial Number: " + str(serialNumber))

kit = InterfaceKit()
kit.setOnAttachHandler(handleAttach)

kit.openPhidget(338807)
kit.setOnInputChangeHandler(inputChanged)
kit.waitForAttach(10000)

raw_input("<(q) quit>")

kit.closePhidget()


