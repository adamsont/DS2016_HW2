__author__ = 'Taavi'

import threading
import Queue
from time import sleep


class Ticker(threading.Thread):
    def __init__(self, func, delay):
        threading.Thread.__init__(self)
        self.func = func
        self.delay = delay
        self.running = True
        self.start()

    def run(self):
        while self.running:
            self.func()
            sleep(self.delay)

    def stop(self):
        self.running = False


class Actor(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.message_queue = Queue.Queue()
        self.tick_in_queue = False
        self.ticker = Ticker(self.internal_tick, 0.5)

    def tick(self):
        raise NotImplementedError

    def internal_tick(self):
        if not self.tick_in_queue:
            self.message_queue.put(self.tick)
            self.tick_in_queue = True

    def run(self):
        while True:
            try:
                f = self.message_queue.get()

                if f == self.tick:
                    self.tick_in_queue = False
                f()
            except Queue.Empty:
                pass
