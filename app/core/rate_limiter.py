from cache.redis_client import redis_client

class RateLimiter:
    
    def __init__(self, limit=100, window = 60) -> None:
        self.limit = limit
        self.window = 60
        
    def allow_request(self, key):
        redis_key = f"rate_limit: {key}"
        current = redis_client.get(redis_key)
        if current is None:
            """First request in this window:
                We create a counter with value 1
                and ser expiration (window time)
            """
            redis_client.set(redis_key, 1, ex=self.window)
            return True
        # convert redis string to integer
        current = int(str(current))
        if current >= self.limit:
            """User exceeded rate limit"""
            return False
        """Increase Request Counter"""
        redis_client.incr(redis_key)
        return True