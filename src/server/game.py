__author__ = 'Taavi'

from common.utilities.actor import *


class Game(Actor):
    def __init__(self, name):
        Actor.__init__(self)
        self.name = name
        self.start()

    def tick(self):
        pass