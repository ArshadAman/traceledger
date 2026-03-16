import time

def retry(opration, retries = 3, delay = 1):
    """
    Generic retry wrapper for temporary failures
    """
    
    for attempt in range(retries):
        try:
            # attempt operation
            return opration()
        except Exception as e:
            print(f"Attempt {attempt+1} failed: ", e)
            time.sleep(delay)
    
    raise Exception("Operation failed after retries")
    