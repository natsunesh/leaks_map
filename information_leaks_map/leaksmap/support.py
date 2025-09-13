"""
Support ticket module for handling user support requests.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket

@login_required
def create_ticket(request):
    """
    Create a new support ticket.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title or not description:
            messages.error(request, 'Both title and description are required')
            return redirect('create_ticket')

        # Create support ticket
        SupportTicket.objects.create(
            user=request.user,
            title=title,
            description=description
        )

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
