import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logger to write into requests.log
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')  # log file at project root
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware to log every incoming HTTP request
    with timestamp, user, and path accessed.
    """
    def __init__(self, get_response):
        self.get_response = get_response  # Django callable to process request

    def __call__(self, request):
        # Get authenticated user or mark as Anonymous
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Prepare log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"

        # Write log to file
        logger.info(log_message)

        # Continue request processing
        response = self.get_response(request)
        return response
