"""
Feedback module for handling user feedback functionality.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Feedback

def submit_feedback(request):
    """
    Handle feedback submission.
    """
    if request.method == 'POST':
        feedback_content = request.POST.get('feedback', '').strip()

        if not feedback_content:
            messages.error(request, 'Feedback cannot be empty')
            return redirect('feedback')

        # Save feedback to database
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            content=feedback_content
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
