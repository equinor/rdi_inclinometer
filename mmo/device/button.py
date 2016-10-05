import time
import thread
import atexit
from threading import Thread
# from Phidgets.PhidgetException import PhidgetException


class Button(object):
    """
    Contains methods to encapsulate long/short press.
    key_pressed is the callback method to use
    """

    down_time = None

    def key_down(self):
        self.down_time = time.clock()

    def key_up(self):
        if self.down_time is not None:
            self.key_pressed(time.clock() - self.down_time)

    def key_pressed(self, param):
        pass

    def beep(self, seconds):
        pass

    @staticmethod
    def get_for_system():
        """
        Returns a phidget button if possible, otherwise it will
        be a keyboard button
        """
        try:
            return RaspberryButton()
        except Exception as e:
            print(e)
            print("Problem initializing Raspberry PI GPIO button"
                  " -- using KeyboardButton.")
            return KeyboardButton()


class RaspberryButton(Button):
    BUTTON1 = 8
    BUTTON2 = 10
    BUZZER = 13

    def __init__(self):
        import RPi.GPIO as GPIO
        Button.__init__(self)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BUZZER, GPIO.OUT)
        GPIO.output(self.BUZZER, GPIO.LOW)
        GPIO.setup(self.BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.BUTTON1, GPIO.FALLING,
                              callback=self.edge, bouncetime=500)
        GPIO.add_event_detect(self.BUTTON2, GPIO.FALLING,
                              callback=self.edge, bouncetime=500)
        atexit.register(GPIO.cleanup)

    def edge(self, pin):
        if pin == self.BUTTON1:
            self.key_pressed(0.2)

        if pin == self.BUTTON2:
            self.key_pressed(1.0)

    def unbeep(self, seconds):
        import RPi.GPIO as GPIO

        def f():
            time.sleep(seconds)
            GPIO.output(self.BUZZER, GPIO.LOW)
        return f

    def beep(self, seconds):
        import RPi.GPIO as GPIO
        GPIO.output(self.BUZZER, GPIO.HIGH)
        t = Thread(target=self.unbeep(seconds))
        t.start()


# class PhidgetButton(Button):
#    from Phidgets.Devices.InterfaceKit import InterfaceKit
#    """
#    Wraps a phidget button
#    """
#    def __init__(self, interface_kit=InterfaceKit()):
#        Button.__init__(self)
#        self.interface_kit = interface_kit
#        interface_kit.openPhidget()
#        interface_kit.setOnInputChangeHandler(self.input_change)
#        try:
#            interface_kit.waitForAttach(1000)
#        except PhidgetException:
#            print "Could not connect to button"
#            raise
#
#    def input_change(self, event):
#        if event.index == 0:
#            if event.state:
#                self.key_down()
#            else:
#                self.key_up()
#
#    def beep(self, seconds):
#        self.interface_kit.setOutputState(0, True)
#        time.sleep(seconds)
#        self.interface_kit.setOutputState(0, False)


class KeyboardButton(Button):
    """
    Emulates a button using keyboard input (for use on PC)
    """

    def __init__(self):
        self.start_input_thread()

    def read_input(self):
        print("Reading keyboard."
              "Press 'a' for short, 's' for long, 'q' for stop")
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

    def beep(self, seconds):
        print("Beep: {}".format(seconds))
