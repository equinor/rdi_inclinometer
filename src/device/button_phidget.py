from Phidgets.PhidgetException import PhidgetException

from device.button import Button


class PhidgetButton(Button):
    from Phidgets.Devices.InterfaceKit import InterfaceKit
    """
    Wraps a phidget button
    """
    def __init__(self, interface_kit=InterfaceKit()):
        Button.__init__(self)
        self.interface_kit = interface_kit
        interface_kit.openPhidget()
        interface_kit.setOnInputChangeHandler(self.input_change)
        try:
            interface_kit.waitForAttach(1000)
        except PhidgetException:
            print "Could not connect to button"
            raise

    def input_change(self, event):
        if event.index == 0:
            if event.state:
                self.key_down()
            else:
                self.key_up()