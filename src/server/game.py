__author__ = 'Taavi'

from common.utilities.actor import *
from server_connection import *
import threading


class Game():
    def __init__(self,name):
        self.name = name
        self.ongoing = False
        self.players = []
        self.current_turn = 0

    def move_next_turn(self):
        self.current_turn += 1

        if self.current_turn > len(self.players) - 1:
            self.current_turn = 0