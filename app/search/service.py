from app.core.circuit_breaker import CircuitBreaker

search_cb = CircuitBreaker(
    failure_threshold=3,
    recovery_time=10
)