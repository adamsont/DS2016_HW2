__author__ = 'Taavi'
import pika
import uuid
import logging
from common.utilities.actor import *
from common.packets import *

import common.protocol as P


class ConnectionActor(Actor):
    def __init__(self):
        Actor.__init__(self)

        self.sync_connection = SynchronizedRequestConnection("lobby")
        self.start()

    def tick(self):
        pass

    #
    # PUBLIC
    #

    def send(self, packet, callback):
        self.message_queue.put(lambda: self.send_handler(packet, callback))

    #
    # PRIVATE
    #

    def send_handler(self, packet, callback):
        response = self.sync_connection.send_receive(packet.serialize())
        callback(response)

class SynchronizedRequestConnection():
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def send_receive(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response