import redis

# initialize the client
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)