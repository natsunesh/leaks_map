from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from information_leaks_map.leaksmap.models import AnalyticsData

@login_required
def analytics(request):
    analytics_data = AnalyticsData.objects.filter(user=request.user)
    return render(request, 'leaksmap/analytics.html', {'analytics_data': analytics_data})
