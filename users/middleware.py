from django.utils import timezone
from django.conf import settings
from django.core.cache import cache


class UserActiveMidlleware:
    "Updates the last_seen status for the user on each request."
    def __init__(self, get_response):
        self._get_response = get_response
    
    def __call__(self, requset):
        current_user = requset.user
        if current_user.is_authenticated:
            now = timezone.now()
            cache.set(f'last_seen_{current_user.id}', now, timeout=settings.USER_LAST_SEEN_TIMEOUT)
        return self._get_response(requset)
