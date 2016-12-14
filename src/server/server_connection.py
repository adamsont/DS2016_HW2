__author__ = 'Taavi'
import pika
import logging


class SynchronizedRequestHandler():
    def __init__(self, channel, queue_name):

        self.channel = channel
        self.queue_name = queue_name

        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_purge(queue_name)
        self.channel.basic_consume(self.on_request, queue=self.queue_name)

    def on_request(self, ch, method, props, body):
        if props.reply_to is None:
            logging.info("SynchronizedRequestHandler NONE")
            return

        response = self.handle_request(body)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def handle_request(self, message):
        raise NotImplementedError