import time


class Timer:
    def __init__(self, text):
        self.start = time.clock()
        self.text = text

    def elapsed(self):
        print("{}: {}s".format(self.text, time.clock() - self.start))