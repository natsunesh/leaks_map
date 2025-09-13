from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Breach

@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        # SupportTicket.objects.create(user=request.user, title=title, description=description)
        return render(request, 'leaksmap/create_ticket.html', {'success': True})
    return render(request, 'leaksmap/create_ticket.html')

@login_required
def view_tickets(request):
    # tickets = SupportTicket.objects.filter(user=request.user)
    # return render(request, 'leaksmap/view_tickets.html', {'tickets': tickets})
    return render(request, 'leaksmap/view_tickets.html')
