import time
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

    def beep(self, seconds):
        pass

    @staticmethod
    def get_for_system():
        """
        Returns a phidget button if possible, otherwise it will be a keyboard button
        """
        try:
            from mmo.device.button_phidget import PhidgetButton
            return PhidgetButton()
        except Exception:
            print "No phidget button detected -- using keyboard button."
            return KeyboardButton()


class KeyboardButton(Button):
    """
    Emulates a button using keyboard input (for use on PC)
    """
    def __init__(self):
        Button.__init__(self)
        self.start_input_thread()

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
