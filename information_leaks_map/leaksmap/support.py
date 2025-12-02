"""
Support ticket module for handling user support requests.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import escape
from .models import SupportTicket
from .utils import sanitize_input
import logging

logger = logging.getLogger(__name__)

@login_required
def create_ticket(request):
    """
    Create a new support ticket with XSS protection.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title or not description:
            messages.error(request, 'Both title and description are required')
            return redirect('create_ticket')

        # Validate length
        if len(title) > 200:
            messages.error(request, 'Title is too long (maximum 200 characters)')
            return redirect('create_ticket')
        
        if len(description) > 5000:
            messages.error(request, 'Description is too long (maximum 5000 characters)')
            return redirect('create_ticket')

        # Sanitize input to prevent XSS
        sanitized_title = sanitize_input(title)
        sanitized_description = sanitize_input(description)

        # Create support ticket
        SupportTicket.objects.create(
            user=request.user,
            title=sanitized_title,
            description=sanitized_description
        )

        # Log ticket creation
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        logger.info(f"Support ticket created by user: {request.user.username} from IP: {ip}")

        messages.success(request, 'Support ticket created successfully')
        return redirect('view_tickets')

    return render(request, 'leaksmap/create_ticket.html')

@login_required
def view_tickets(request):
    """
    View all support tickets for the current user.
    """
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'leaksmap/view_tickets.html', {'tickets': tickets})
