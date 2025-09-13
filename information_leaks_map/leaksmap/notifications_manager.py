from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.filter(user=request.user)
        return render(request, 'leaksmap/notifications.html', {'notifications': notifications})
    elif request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.mark_as_read()
            return JsonResponse({'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return JsonResponse({'error': 'Notification not found'}, status=404)
    return render(request, 'leaksmap/home.html')
