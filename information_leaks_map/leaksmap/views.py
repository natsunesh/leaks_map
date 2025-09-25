"""
Views for the LeaksMap application.
This module contains the view functions for handling web requests.
"""

from django.shortcuts import render
from django.http import JsonResponse
from .utils import validate_email
from .api_client import LeakCheckAPIClient
from .models import Breach
from .export import generate_pdf_report, generate_html_report
from .visualizer import create_breach_visualization
import os

def home(request):
    """
    Render the home page.
    """
    return render(request, 'leaksmap/home.html')

def check_leaks(request):
    """
    Check for data breaches associated with a given email address.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email')
    if not validate_email(email):
        return JsonResponse({'error': 'Invalid email address'}, status=400)

    api_key = os.getenv("API_KEY")
    if not api_key:
        return JsonResponse({'error': 'API key not configured'}, status=500)

    api_client = LeakCheckAPIClient(api_key=api_key)
    breaches = api_client.get_breach_info(email)

    if breaches:
        # Save breaches to database
        for breach in breaches:
            Breach.objects.create(
                service_name=breach['service_name'],
                breach_date=breach['breach_date'],
                description=breach['description']
            )

        return JsonResponse({
            'breaches': breaches,
            'message': 'Breaches found'
        })
    else:
        return JsonResponse({'message': 'No breaches found'}, status=200)

def export_report(request):
    """
    Generate and export a report in PDF or HTML format.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email')
    if not validate_email(email):
        return JsonResponse({'error': 'Invalid email address'}, status=400)

    try:
        breaches = Breach.objects.filter(email=email)
        if not breaches.exists():
            return JsonResponse({'message': 'No breaches found to export'}, status=200)

        format = request.POST.get('format', 'pdf')
        if format == 'pdf':
            return generate_pdf_report(breaches)
        elif format == 'html':
            return generate_html_report(breaches)
        else:
            return JsonResponse({'error': 'Unsupported format'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def visualize_breaches(request):
    """
    Generate and display a visualization of breaches.
    """
    visualization = create_breach_visualization()
    if visualization:
        return render(request, 'leaksmap/visualization.html', {'visualization': visualization})
    else:
        return JsonResponse({'message': 'No breaches found to visualize'}, status=200)
