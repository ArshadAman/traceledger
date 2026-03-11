import pika

def get_rabbit_con():
    params = pika.ConnectionParameters(
        host="localhost"
    )
    
    connection = pika.BlockingConnection(params)
    return connection