"""
Rate limiting decorator to prevent brute force attacks.
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
import time
import logging

logger = logging.getLogger(__name__)

def rate_limit(max_attempts=5, window=300, key_func=None):
    """
    Decorator to limit the number of requests per IP address.
    
    :param max_attempts: Maximum number of attempts allowed
    :param window: Time window in seconds (default: 5 minutes)
    :param key_func: Function to generate cache key (default: uses IP address)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            # Generate cache key
            if key_func:
                cache_key = key_func(request)
            else:
                cache_key = f'rate_limit_{ip}_{view_func.__name__}'
            
            # Check current attempts
            attempts = cache.get(cache_key, 0)
            
            if attempts >= max_attempts:
                logger.warning(f"Rate limit exceeded for IP: {ip}, function: {view_func.__name__}")
                messages.error(request, f'Слишком много попыток. Попробуйте через {window // 60} минут.')
                # Return appropriate response based on request method
                if request.method == 'GET':
                    from django.shortcuts import render
                    from django.http import HttpResponse
                    return HttpResponse(
                        f'<html><body><h1>429 Too Many Requests</h1><p>Слишком много попыток. Попробуйте через {window // 60} минут.</p></body></html>',
                        status=429
                    )
                else:
                    return JsonResponse({
                        'error': 'Rate limit exceeded',
                        'message': f'Слишком много попыток. Попробуйте через {window // 60} минут.'
                    }, status=429)
            
            # Increment attempts
            cache.set(cache_key, attempts + 1, window)
            
            # Call the view function
            response = view_func(request, *args, **kwargs)
            
            # Reset attempts on success (for login, check if login was successful)
            if hasattr(response, 'status_code') and response.status_code == 200:
                if hasattr(request, 'user') and request.user.is_authenticated:
                    cache.delete(cache_key)
            
            return response
        return wrapper
    return decorator



