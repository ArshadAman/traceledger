import time

class CircuitBreaker:
    """
    Circuit braker implementaion
    Purpose:
        Prevent repeated calls to failing services
    """
    
    def __init__(self, failure_threshold=3, recovery_time=10):
        # number of failures allowed before opening a circuit
        self.failure_threshold = failure_threshold
        
        # seconds before attempting recovery
        self.recovery_time = recovery_time
        
        # curent number of failures
        self.failure_count = 0
        
        # state of circuit
        self.state = "CLOSED"
        
        # timestamp when circuit opened
        self.last_failure_time = None
        
    def call(self, func, *args, **kwargs):
        """
        Execute the protected function.
        func -> function we want to execute
        args/kwargs -> parameters of the function
        """
        # If circuit is Open, check if recovery time is passed
        if self.state == "OPEN":
            if self.last_failure_time and time.time() - self.last_failure_time > self.recovery_time:
                # Move to half open state
                self.state = "HALF_OPEN"
            else:
                # Service is still blocked
                raise Exception("Circuit is OPEN, service UNAVAILABLE")
        
        try:
            # Execute the funciton
            result = func(*args, **kwargs)
            
            # If HALF_OPEN successds, close the circuit
            if self.state == 'HALF_OPEN':
                self.reset()
            return result
        except Exception as e:
            # logs error
            # increase failure count
            self.failure_count +=1 
            
            # if the threshold reached -> OPEN cuitcuit
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise e
    
    def reset(self):
        # Reset the circuit breaker
        self.failure_count = 0
        self.state = "CLOSED"