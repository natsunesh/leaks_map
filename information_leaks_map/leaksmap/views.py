from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Breach
from .utils import validate_email
from .api_client import LeakCheckAPIClient
from .visualizer import create_breach_visualization
from .notifications import notify_user
from .recommendations import generate_checklist, get_security_advice
from .export import generate_pdf_report, generate_html_report
import os

def home(request):
    return render(request, 'leaksmap/home.html')

def check_leaks(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not validate_email(email):
            return JsonResponse({'error': 'Invalid email address'}, status=400)

        api_key = os.getenv("API_KEY")
        if not api_key:
            return JsonResponse({'error': 'API key not configured'}, status=500)
        api_client = LeakCheckAPIClient(api_key=api_key)
        # Get breach information from the API
        breaches = api_client.get_breach_info(email)

        # Check if breaches are found
        if breaches:
            # Save each breach to the database
            for breach in breaches:
                Breach.objects.create(
                    service_name=breach['service_name'],
                    breach_date=breach['breach_date'],
                    description=breach['description']
                )
            # Send notifications to the user
            notification_message = f"New data breach detected for email: {email}"
            notify_user(email, notification_message)
            # Generate recommendations and security advice
            checklist = generate_checklist(email)
            security_advice = get_security_advice()
            return JsonResponse({'breaches': breaches, 'checklist': checklist, 'security_advice': security_advice})
        else:
            # Return a message if no breaches are found
            return JsonResponse({'message': 'No breaches found'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def export_report(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not validate_email(email):
            return JsonResponse({'error': 'Invalid email address'}, status=400)

        try:
            breaches = Breach.objects.select_related().filter(email=email)
            if breaches.exists():
                format = request.POST.get('format', 'pdf')
                if format == 'pdf':
                    return generate_pdf_report(breaches)
                elif format == 'html':
                    return generate_html_report(breaches)
                else:
                    return JsonResponse({'error': 'Unsupported format'}, status=400)
            else:
                return JsonResponse({'message': 'No breaches found to export'}, status=200)
        except Breach.DoesNotExist:
            return JsonResponse({'message': 'No breaches found to export'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def visualize_breaches(request):
    if request.method == 'GET':
        visualization = create_breach_visualization()
        return render(request, 'leaksmap/visualization.html', {'visualization': visualization})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
