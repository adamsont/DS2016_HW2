__author__ = 'Taavi'

from common.utilities.actor import *
from server_connection import *
import threading


class Game():
    def __init__(self,name):
        self.name = name
        players = []
