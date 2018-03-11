import pika

url = 'amqp://user:password@host/XXX'
parameters = pika.URLParameters(url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='offer.verification.request')

channel.basic_publish(exchange='',
                      routing_key='offer.verification.request',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
