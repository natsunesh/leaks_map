from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'leaksmap/notifications.html', {'notifications': notifications})
