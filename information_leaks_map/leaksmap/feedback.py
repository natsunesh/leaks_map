"""
Feedback module for handling user feedback functionality.
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils.html import escape
from .models import Feedback
from .rate_limit import rate_limit
import logging

logger = logging.getLogger(__name__)

def sanitize_feedback_content(content: str) -> str:
    """
    Sanitize feedback content to prevent XSS attacks.
    
    :param content: Raw feedback content
    :return: Sanitized content
    """
    # Remove script tags and dangerous HTML
    import re
    # Remove script tags
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    # Remove event handlers
    content = re.sub(r'on\w+\s*=', '', content, flags=re.IGNORECASE)
    # Remove javascript: protocol
    content = re.sub(r'javascript:', '', content, flags=re.IGNORECASE)
    # Escape HTML but preserve line breaks
    content = escape(content)
    return content

@rate_limit(max_attempts=10, window=3600)  # 10 попыток в час
def submit_feedback(request):
    """
    Handle feedback submission with XSS protection and rate limiting.
    """
    if request.method == 'POST':
        feedback_content = request.POST.get('feedback', '').strip()

        if not feedback_content:
            messages.error(request, 'Feedback cannot be empty')
            return redirect('feedback')

        # Validate length
        if len(feedback_content) > 5000:
            messages.error(request, 'Feedback is too long (maximum 5000 characters)')
            return redirect('feedback')

        # Sanitize content to prevent XSS
        sanitized_content = sanitize_feedback_content(feedback_content)

        # Log submission
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        logger.info(f"Feedback submitted from IP: {ip}, user: {request.user.username if request.user.is_authenticated else 'anonymous'}")

        # Save feedback to database
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            content=sanitized_content
        )

        messages.success(request, 'Feedback submitted successfully')
        return redirect('feedback')

    return render(request, 'leaksmap/feedback.html')

def view_feedback(request):
    """
    Display all submitted feedback.
    """
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'leaksmap/view_feedback.html', {'feedbacks': feedbacks})
