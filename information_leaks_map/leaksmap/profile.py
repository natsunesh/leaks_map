from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_profile.first_name = request.POST.get('first_name', '')
        user_profile.last_name = request.POST.get('last_name', '')
        user_profile.email = request.POST.get('email', '')
        user_profile.save()
        return render(request, 'leaksmap/profile.html', {'user_profile': user_profile, 'success': True})

    return render(request, 'leaksmap/profile.html', {'user_profile': user_profile})
