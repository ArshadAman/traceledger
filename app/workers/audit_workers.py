import json
from db.pool import pool
from db.connection import get_db_conn
from psycopg2.extras import RealDictCursor
from db.audit import INSERT_AUDIT_EVENT
from messaging.rabbitmq import get_rabbit_con

# callback function
def handle_event(ch, method, properties, body):
    
    # convert bytes -> json
    event = json.loads(body)
    event_type = event["event_type"]
    data = event["data"]
    
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(
                    INSERT_AUDIT_EVENT,
                    (
                        data.get("user_id"),
                        "user",
                        event_type,
                        "login",
                        data["status"],
                        json.dumps(data)
                    )
                )
            conn.commit()
    finally:
        pool.putconn(conn)
    
    # Tell RabbitMQ message is processed
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
def main():
    connection = get_rabbit_con()
    channel = connection.channel()

    channel.exchange_declare(
        exchange="audit_events",
        exchange_type="fanout"
    )
    
    # Create a queue
    result = channel.queue_declare(queue="audit_events_queue", durable=True)
    queue_name = result.method.queue
    channel.queue_bind(
        exchange="audit_events",
        queue = queue_name
    )
    
    # start consuming message
    channel.basic_consume(
        queue=queue_name,
        on_message_callback = handle_event,
        auto_ack=False
    )
    
    print("Audit worker running.....")
    channel.start_consuming()
    
if __name__ == "__main__":
    main()