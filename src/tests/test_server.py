import pika


class SynchronizedRequestHandler():
    def __init__(self, queue_name):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        channel = connection.channel()

        channel.queue_declare(queue=queue_name)
        channel.basic_consume(self.on_request, queue=queue_name)
        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        if props.reply_to is None:
            return

        if body == "Hello":
            response = "Hello you too!"
        else:
            response = "Unknown request"

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


handler = SynchronizedRequestHandler('hello')