from threading import Thread
import atexit


class Voice:
    def __init__(self):
        import pyttsx
        self.engine = pyttsx.init()

        self.thread = Thread(target=self._start_loop)
        self.thread.daemon = True
        self.thread.start()
        atexit.register(self.stop_loop_thread)

    def say(self, text):
        self.engine.say(text)

    def _start_loop(self):
        self.engine.startLoop()

    def stop_loop_thread(self):
        self.engine.endLoop()
        self.thread.join()
