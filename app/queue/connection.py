import pika

# connect to the host
def rmq_connect():
    params = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(params)
    return connection