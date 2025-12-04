from typing import List, Union
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import os
import asyncio
from asgiref.sync import sync_to_async
from .api_client import LeakCheckAPIClient
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Breach
import logging
from django.shortcuts import render
from .forms import RegistrationForm, LoginForm, CheckBreachesForm, ExportReportForm

logger = logging.getLogger(__name__)

@login_required
@csrf_protect
def get_security_advice(request, breaches: List[Breach]) -> JsonResponse:
    """
    Generate personalized security advice based on the user's breaches.
    """
    try:
        # Group breaches by service for service-specific advice
        service_breaches = {}
        for breach in breaches:
            service = breach.service_name
            if service not in service_breaches:
                service_breaches[service] = []
            service_breaches[service].append(breach)

        # Generate service-specific advice
        service_advice = {}
        for service, service_breach_list in service_breaches.items():
            service_advice[service] = generate_service_security_advice(service_breach_list)

        # Combine all advice into a single string
        security_advice = "".join(service_advice.values())
        return JsonResponse({"advice": security_advice})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@csrf_protect
def generate_service_security_advice(breaches: List[Breach]) -> JsonResponse:
    """
    Generate service-specific security advice based on the user's breaches.
    """
    try:
        # Generate advice for each breach
        advice_list = [generate_security_advice_for_breach(breach) for breach in breaches]
        # Combine all advice into a single string
        advice = "".join([a["advice"] for a in advice_list])
        return JsonResponse({"advice": advice})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@csrf_protect
def generate_security_advice_for_breach(breach: Breach) -> JsonResponse:
    """
    Generate security advice based on a single breach.
    """
    try:
        advice = ""
        if breach.service_name:
            advice += f"Change your password for {breach.service_name}\n"
        if breach.data_type:
            advice += f"Check your {breach.data_type} for any suspicious activity\n"
        return JsonResponse({"advice": advice})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@csrf_exempt
def check_leaks(request) -> JsonResponse:
    if request.method == 'POST':
        form = CheckBreachesForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Initialize LeakCheck API client
            api_key = os.getenv('LEAKCHECK_API_KEY')
            if not api_key:
                return JsonResponse({"error": "LeakCheck API key is not configured"}, status=500)

            client = LeakCheckAPIClient(api_key)
            breaches = asyncio.run(client.get_breach_info_by_email(email))
            logger.debug(f"Breaches data: {breaches}")
            logger.debug(f"API response: {breaches}")

            if not breaches:
                return JsonResponse({"status": "success", "message": "No breaches found"})

            # Save breaches to the database
            for breach_data in breaches:
                Breach.objects.create(
                    user=request.user,
                    service_name=breach_data["service_name"],
                    breach_date=breach_data["breach_date"],
                    location=breach_data.get("location", "Unknown"),
                    data_type=breach_data.get("data_type", "Unknown"),
                    description=breach_data.get("description", "No description"),
                    source=breach_data.get("source", "Unknown")
                )

            return JsonResponse({"status": "success", "message": "Leaks check completed", "breaches": breaches})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
@csrf_protect
def user_logout(request) -> HttpResponseRedirect:
    """
    Log out the user.
    """
    logout(request)
    # Always redirect to the register page
    return HttpResponseRedirect('/register/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
    return render(request, 'registration/register.html', {'form': form})

@csrf_protect
def edit_profile(request) -> HttpResponseRedirect:
    """
    Handle profile editing.
    """
    if request.method == 'POST':
        # Placeholder for the actual implementation
        return HttpResponseRedirect('/edit_profile/')
    return HttpResponseRedirect('/edit_profile/')

@login_required
@csrf_protect
def view_profile(request) -> HttpResponseRedirect:
    """
    View user profile.
    """
    if request.method == 'GET':
        # Placeholder for the actual implementation
        return HttpResponseRedirect('/view_profile/')
    return HttpResponseRedirect('/view_profile/')

@login_required
@csrf_protect
def visualize_breaches(request) -> JsonResponse:
    if request.method == 'GET':
        # Получаем параметры фильтрации и сортировки из запроса
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        search_term = request.GET.get('search')
        sort_field = request.GET.get('sort')

        # Фильтруем и сортируем утечки
        breaches = Breach.objects.all()
        if start_date:
            breaches = breaches.filter(breach_date__gte=start_date)
        if end_date:
            breaches = breaches.filter(breach_date__lte=end_date)
        if search_term:
            breaches = breaches.filter(service_name__icontains=search_term)
        if sort_field:
            breaches = breaches.order_by(sort_field)

        data = {
            "breaches": list(breaches.values("service_name", "breach_date", "location", "data_type", "description")),
            "total_breaches": breaches.count()
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request method"}, status=400)
    """
    Visualize breaches.
    """
    if request.method == 'GET':
        breaches = Breach.objects.all()  # Replace with actual logic to fetch breaches
        data = {
            "breaches": list(breaches.values("service_name", "breach_date", "location", "data_type", "description")),
            "total_breaches": breaches.count()
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
@csrf_protect
def home_view(request):
    """
    Handle home page.
    """
    if request.method == 'GET':
        return render(request, 'leaksmap/home.html')
    return HttpResponseRedirect('/')

@login_required
@csrf_protect
def chronological_journal(request) -> JsonResponse:
    """
    Handle chronological journal.
    """
    if request.method == 'GET':
        breaches = Breach.objects.all().order_by('-breach_date')  # Replace with actual logic to fetch breaches
        data = {
            "breaches": list(breaches.values("service_name", "breach_date", "location", "data_type", "description")),
            "total_breaches": breaches.count()
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
@csrf_protect
def help_page(request) -> JsonResponse:
    """
    Handle help page.
    """
    if request.method == 'GET':
        # Placeholder for the actual implementation
        return JsonResponse({"status": "success", "message": "Help page implemented"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
@csrf_protect
def export_report(request) -> HttpResponse:
    if request.method == 'POST':
        form = ExportReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            breaches = Breach.objects.filter(user=request.user)

            if report_type == 'PDF':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                # Generate PDF report (placeholder)
                response.write(b"PDF report content")
                return response
            elif report_type == 'HTML':
                response = HttpResponse(content_type='text/html')
                response['Content-Disposition'] = 'attachment; filename="report.html"'
                # Generate HTML report (placeholder)
                response.write("<html><body>HTML report content</body></html>")
                return response
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"error": "Invalid request method"}, status=400)
