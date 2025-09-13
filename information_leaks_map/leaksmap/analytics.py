from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Breach

@login_required
def analytics(request):
    # analytics_data = AnalyticsData.objects.filter(user=request.user)
    # return render(request, 'leaksmap/analytics.html', {'analytics_data': analytics_data})
    return render(request, 'leaksmap/analytics.html')
