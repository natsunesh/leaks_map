from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification, User

def notify_user(email, message):
    # Implement the logic to notify the user
    pass

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'leaksmap/notifications.html', {'notifications': notifications})
