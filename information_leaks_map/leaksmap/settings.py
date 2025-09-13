from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserSettings

@login_required
def settings(request):
    try:
        user_settings = UserSettings.objects.get(user=request.user)
    except UserSettings.DoesNotExist:
        user_settings = UserSettings.objects.create(user=request.user)

    if request.method == 'POST':
        user_settings.notification_enabled = request.POST.get('notification_enabled', 'off') == 'on'
        user_settings.dark_mode = request.POST.get('dark_mode', 'off') == 'on'
        user_settings.save()
        return render(request, 'leaksmap/settings.html', {'user_settings': user_settings, 'success': True})

    return render(request, 'leaksmap/settings.html', {'user_settings': user_settings})
