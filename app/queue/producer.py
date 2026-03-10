import connection

# Get the channel
connect = connection.rmq_connect()
channel = connect.channel()

# declare the queue/use if exits
channel.queue_declare(queue="audit_queue")

# publish a message to rabbit mq
channel.basic_publish(
    exchange="",
    routing_key="audit_queue",
    body="USER_LOGGEG_IN"
)
print("Message sent to audit queue")
connect.close()