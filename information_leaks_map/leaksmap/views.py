from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Breach
from .utils import validate_email
from .api_client import LeakCheckAPIClient
import os

def home(request):
    return render(request, 'leaksmap/home.html')

def check_leaks(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not validate_email(email):
            return JsonResponse({'error': 'Invalid email address'}, status=400)

        api_client = LeakCheckAPIClient(api_key=os.getenv("API_KEY", "ace07ec3058ee59cabf16c86b0d2e5842060ee41"))
        breaches = api_client.get_breach_info(email)

        if breaches:
            for breach in breaches:
                Breach.objects.create(
                    service_name=breach['service_name'],
                    breach_date=breach['breach_date'],
                    description=breach['description']
                )
            return JsonResponse({'breaches': breaches})
        else:
            return JsonResponse({'message': 'No breaches found'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def export_report(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not validate_email(email):
            return JsonResponse({'error': 'Invalid email address'}, status=400)

        breaches = Breach.objects.filter(service_name__icontains=email)
        if breaches.exists():
            report_content = ""
            for breach in breaches:
                report_content += f"Service: {breach.service_name}\n"
                report_content += f"Breach Date: {breach.breach_date}\n"
                report_content += f"Description: {breach.description}\n\n"

            response = HttpResponse(report_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{email}_report.txt"'
            return response
        else:
            return JsonResponse({'message': 'No breaches found to export'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
