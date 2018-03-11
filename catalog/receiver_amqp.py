import pika

url = 'amqp://user:password@host/XXX'
parameters = pika.URLParameters(url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='offer.verification.response')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='offer.verification.response',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
