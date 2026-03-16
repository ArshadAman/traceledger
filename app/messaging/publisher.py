import json
from messaging.rabbitmq import get_rabbit_con
import pika

def publish_event(event_type, payload):
    try:
        connection = get_rabbit_con()
        
        channel = connection.channel()
        
        # Declare exchange
        channel.exchange_declare(
            exchange="audit_events",
            exchange_type="fanout",
            durable=True
        )
        
        # Prepare message
        message = {
            "event_type": event_type,
            "data": payload
        }
        
        channel.basic_publish(
            exchange="audit_events",
            routing_key="",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print("Rabbit MQ degraded: ", e)