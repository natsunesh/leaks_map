from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recommendation

@login_required
def recommendations(request):
    recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'leaksmap/recommendations.html', {'recommendations': recommendations})
