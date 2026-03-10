import connection
connect = connection.rmq_connect()
channel = connect.channel()

# declare or use the queue
channel.queue_declare(queue="audit_queue")

# callback function to run after consuming
def do_work(ch, method, properties, body):
    # proccess the task
    for i in range(10):
        print(i)
    print("Message received: ", body.decode())
    
    
# Consume from the queue
channel.basic_consume(
    queue="audit_queue",
    on_message_callback=do_work,
    auto_ack=True
)

print("Wating for message....")
# Channel will keep running and process the messages as they arrive
channel.start_consuming()