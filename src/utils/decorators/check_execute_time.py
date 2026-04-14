import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def check_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info("Execution time for %s: %.4f seconds", func.__name__, execution_time)
        return result
    return wrapper
