from prometheus_client import Counter

# Simple in-memory metrics

# Counter -> total_request
REQUEST_COUNT = 0

# Counter -> Failed Request
ERROR_COUNT = 0

# Counter -> login attempts
LOGIN_COUNT = 0


def increment_request():
    """This function inccreases request count by 1
    Called everytime API hits
    """
    global REQUEST_COUNT
    REQUEST_COUNT+=1

def increment_error():
    """Increase error count Called when exception occurs"""
    global ERROR_COUNT
    ERROR_COUNT+=1

def increment_login():
    """Track Loggin Attemps"""
    global LOGIN_COUNT
    LOGIN_COUNT +=1

def get_metrics():
    """Returns all metrics as dictionary"""
    return {
        "total_request": REQUEST_COUNT,
        "total_errors": ERROR_COUNT,
        "total_requests": LOGIN_COUNT,
    }
    

login_success_counter = Counter(
    "login_success_total",
    "Total successful logins"
)

login_failure_counter = Counter(
    "login_failure_total",
    "Total failed logins"
)