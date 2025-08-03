import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted at this time."
            )
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track requests per IP: {ip: [timestamps]}
        self.requests_per_ip = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean timestamps older than 1 minute
            self.requests_per_ip[ip] = [
                ts for ts in self.requests_per_ip[ip]
                if now - ts < timedelta(minutes=1)
            ]

            # Check limit
            if len(self.requests_per_ip[ip]) >= 5:
                return HttpResponseForbidden(
                    "Message limit exceeded. Try again later."
                )

            # Log current request timestamp
            self.requests_per_ip[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Extract client IP address from headers or META
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Check authentication
        if user.is_authenticated:
            # Assume User model has `role` attribute
            role = getattr(user, 'role', None)
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden(
                    "You do not have permission to perform this action."
                )
        else:
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
