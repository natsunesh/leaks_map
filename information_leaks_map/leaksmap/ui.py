from django.shortcuts import render
from .models import Breach

def display_results(request):
    if request.method == 'GET':
        breaches = Breach.objects.all()
        return render(request, 'leaksmap/results.html', {'breaches': breaches})
    return render(request, 'leaksmap/home.html')
