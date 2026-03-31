import pika
from app.core.config import settings

def get_rabbit_con():
    params = pika.ConnectionParameters(
        host=settings.rabbitmq_host
    )
    
    connection = pika.BlockingConnection(params)
    return connection