import boto3, pika

from django.conf import settings

# Create SQS client
client = boto3.client('sqs',
                      aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                      region_name = settings.AWS_REGION,
                     )

def send_message_sqs(queue, message):
    queues = client.list_queues(QueueNamePrefix=queue)
    queue_url = queues['QueueUrls'][0]

    # Send message to SQS queue
    response = client.send_message(
        QueueUrl = queue_url,
        DelaySeconds = 10,
        MessageBody = message
    )
    return response['MessageId']

def send_message_rabbit(queue, message):
    parameters = pika.URLParameters(settings.URL_BROKER)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=str(message))
    print(" [x] Message sent successfully")
    connection.close()

def receive_message_rabbit(queue, callback):
    parameters = pika.URLParameters(settings.URL_BROKER)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
