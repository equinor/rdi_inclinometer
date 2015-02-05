import time
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.PhidgetException import PhidgetException
import thread
from threading import Thread

class Button:
    """
    Contains methods to encapsulate long/short press. key_pressed is the callback method to use
    """
    def __init__(self):
        self.down_time = None

    def key_down(self):
        self.down_time = time.clock()

    def key_up(self):
        self.key_pressed(time.clock() - self.down_time)

    def key_pressed(self, param):
        pass

    @staticmethod
    def get_for_system():
        """
        Returns a phidget button if possible, otherwise it will be a keyboard button
        """
        try:
            return PhidgetButton()
        except Exception:
            print "No phidget button detected -- using keyboard button."
            kb = KeyboardButton()
            kb.start_input_thread()
            return kb



class PhidgetButton(Button):
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


class KeyboardButton(Button):
    """
    Emulates a button using keyboard input (for use on PC)
    """
    def __init__(self):
        Button.__init__(self)

    def read_input(self):
        print "Reading keyboard. Press 'a' for short, 's' for long, 'q' for stop"
        while True:
            key = raw_input()
            if key == "q":
                print "Q was pressed. Namaste!"
                break
            elif key == "a":
                self.key_pressed(0.2)
            elif key == "s":
                self.key_pressed(1.0)
        thread.interrupt_main()

    def start_input_thread(self):
        t = Thread(target=self.read_input)
        t.start()
