from app.core.logger import logger
import json
from app.search.client import index_audit_event
from datetime import datetime
from app.db.audit import INSERT_AUDIT_EVENT
from app.db.connection import get_db_conn
from app.db.pool import pool
from app.messaging.rabbitmq import get_rabbit_con
from psycopg2.extras import RealDictCursor


# Event Processing
def process_event(event):
    """Business logic for processing audit event"""
    event_type = event["event_type"]
    data = event["data"]

    conn = get_db_conn()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                INSERT_AUDIT_EVENT,
                (
                    data.get("user_id"),
                    "user",
                    event_type,
                    "login",
                    data.get("status", "unknown"),
                    json.dumps(data),
                ),
            )

            conn.commit()
        
        doc = {
            "actor_id": data.get("user_id"),
            "action": event_type,
            "status": data.get("status", "unknown"),
            "metadata": data,
            "timestamp": datetime.utcnow().isoformat(),
            "message": data.get("reason", ""),
        }
        
        index_audit_event(doc)

    finally:
        pool.putconn(conn)


# Worker callback
def handle_event(ch, method, properties, body):
    """Rabbit MQ handler"""
    logger.info("handler started.....")
    try:
        event = json.loads(body)

        # Process event
        process_event(event)
        # Success -> ack message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error("Worker Failed: ", e)
        # retry count tracking
        retry_count = 0
        if properties.headers and "x-retry-count" in properties.headers:
            retry_count = properties.headers["x-retry-count"]

        # Max retry attempts
        MAX_RETRY = 3

        if retry_count < MAX_RETRY:
            logger.warning("Retrying message: ", retry_count + 1)

            # Publish message to retry exchange
            ch.basic_publish(
                exchange="audit_events_retry",
                routing_key="",
                body=body,
                properties=properties.__class__(
                    headers={"x-retry-count": retry_count + 1},
                    delivery_mode=2,
                ),
            )

            # ack original message
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logger.info("Sending to DLQ....")
            # reject message -> goes to DLQ
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


# Main Worker
def main():
    connection = get_rabbit_con()
    channel = connection.channel()

    # Main exchange
    channel.exchange_declare(
        exchange="audit_events", exchange_type="fanout", durable=True
    )

    # Retry exchange
    channel.exchange_declare(
        exchange="audit_events_retry", exchange_type="fanout", durable=True
    )

    # ---------- DLQ EXCHANGE ----------
    channel.exchange_declare(
        exchange="audit_events_dlx", exchange_type="fanout", durable=True
    )

    # ---------- DEAD LETTER QUEUE ----------
    channel.queue_declare(queue="audit_events_dlq", durable=True)

    channel.queue_bind(exchange="audit_events_dlx", queue="audit_events_dlq")

    # ---------- RETRY QUEUE ----------
    channel.queue_declare(
        queue="audit_events_retry_queue",
        durable=True,
        arguments={
            "x-message-ttl": 5000,  # retry delay (5 seconds)
            "x-dead-letter-exchange": "audit_events",
        },
    )

    channel.queue_bind(exchange="audit_events_retry", queue="audit_events_retry_queue")

    # ---------- MAIN QUEUE ----------
    channel.queue_declare(
        queue="audit_events_queue",
        durable=True,
        arguments={"x-dead-letter-exchange": "audit_events_dlx"},
    )

    channel.queue_bind(exchange="audit_events", queue="audit_events_queue")

    # limit number of unacknowledged messages
    channel.basic_qos(prefetch_count=10)

    # start consuming
    channel.basic_consume(
        queue="audit_events_queue", on_message_callback=handle_event, auto_ack=False
    )

    logger.info("Audit worker running...")

    channel.start_consuming()


if __name__ == "__main__":
    main()
