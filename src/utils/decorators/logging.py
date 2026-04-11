import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_api_decorator(func):
    def wrapper_function(*args, **kwargs):
        logging.info(f"Calling API: {func.__name__}")
        try:
            response = func(*args, **kwargs)
            logging.info(f"API {func.__name__} called successfully with status: {response.status_code}")
            return response
        except Exception as e:
            logging.error(f"Error while calling API {func.__name__}: {e}")
            raise
    return wrapper_function
