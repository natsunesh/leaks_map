from django.shortcuts import render
from .models import Breach

def display_results(request):
    if request.method == 'GET':
        try:
            breaches = Breach.objects.all()
        except Breach.DoesNotExist:
            breaches = []
        return render(request, 'leaksmap/results.html', {'breaches': breaches})
    return render(request, 'leaksmap/home.html')
