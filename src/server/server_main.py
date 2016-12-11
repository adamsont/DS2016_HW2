__author__ = 'Taavi'

__author__ = 'Taavi'

import pika
import logging
from lobby import *

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

lobby = Lobby(channel, "lobby")