from threading import Thread


class Voice:
    def __init__(self):
        import pyttsx
        self.engine = pyttsx.init()

    def say(self, text):
        self.engine.say(text)

    def _start_loop(self):
        self.engine.startLoop()

    def start_loop_thread(self):
        thread = Thread(target=self._start_loop)
        thread.start()