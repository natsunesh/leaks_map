
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any, List, Union
from .utils import validate_email, sanitize_input, log_security_event, check_password_strength
from .api_client import LeakCheckAPIClient, HaveIBeenPwnedAPIClient
from .models import Breach, Report, UserProfile
from .export import generate_pdf_report, generate_html_report
from .visualizer import create_breach_visualization, create_breach_visualization_from_api, create_breach_map
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def home(request) -> HttpResponse:
    """
    Render the home page.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    return render(request, 'leaksmap/home.html')

@method_decorator(login_required, name='dispatch')
async def check_leaks(request) -> JsonResponse:
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email', request.user.email)
if email is not None:
    email = request.user.email
if email is None:
        if request.user.is_authenticated:
            log_security_event('invalid_email', request.user.pk, f"Email is None")
        else:
            log_security_event('invalid_email', None, f"Email is None")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)
    if email is None:
        if request.user.is_authenticated:
            log_security_event('invalid_email', request.user.pk, f"Email is None")
        else:
            log_security_event('invalid_email', None, f"Email is None")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    email = sanitize_input(email)
    if not validate_email(email):
        if request.user.is_authenticated:
            log_security_event('invalid_email', request.user.pk, f"Invalid email format: {email}")
        else:
            log_security_event('invalid_email', None, f"Invalid email format: {email}")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    all_breaches = []

    # LeakCheck API
    leakcheck_api_key = os.getenv("API_KEY")
    if leakcheck_api_key:
        try:
            leakcheck_client = LeakCheckAPIClient(api_key=leakcheck_api_key)
            leakcheck_breaches = await leakcheck_client._fetch_data_leakcheck(email) or []
            all_breaches.extend(leakcheck_breaches)
        except Exception as e:
            logger.error(f"LeakCheck API error: {str(e)}")
            return JsonResponse({'error': f"LeakCheck API error: {str(e)}"}, status=500)

    # Have I Been Pwned API
    hibp_api_key = os.getenv("HIBP_API_KEY")
    if hibp_api_key:
        try:
            hibp_client = HaveIBeenPwnedAPIClient(api_key=hibp_api_key)
            hibp_breaches = hibp_client.get_breach_info_hibp(email) or []
            all_breaches.extend(hibp_breaches)
        except Exception as e:
            logger.error(f"Have I Been Pwned API error: {str(e)}")
            return JsonResponse({'error': f"Have I Been Pwned API error: {str(e)}"}, status=500)

    if all_breaches:
        # Save breaches to database
        for breach in all_breaches:
            try:
                # Handle date format from API (YYYY-MM)
                breach_date = breach.get('breach_date', '2000-01-01')
                if breach_date and len(breach_date) == 7:  # Format: YYYY-MM
                    breach_date = datetime.strptime(breach_date, '%Y-%m').strftime('%Y-%m-%d')

                # Ensure all required fields are present
                service_name = breach.get('service_name', 'Unknown')
                description = breach.get('description', 'No description')
                source = breach.get('source', 'Unknown')
                data_type = breach.get('data_type', 'Unknown')
                location = breach.get('location', 'Unknown')

                # Create or update breach record
                Breach.objects.get_or_create(
                    user=request.user,
                    service_name=service_name,
                    breach_date=breach_date,
                    description=description,
                    source=source,
                    data_type=data_type,
                    location=location,
                )
            except ValidationError as e:
                logger.error(f"Validation error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=400)

        if request.user.is_authenticated:
            log_security_event('data_breach_found', request.user.pk, f"Found {len(all_breaches)} breaches for {email}")
        else:
            log_security_event('data_breach_found', None, f"Found {len(all_breaches)} breaches for {email}")
        return JsonResponse({
            'breaches': all_breaches,
            'message': 'Breaches found',
            'redirect_url': f'/visualize_breaches/?email={email}'
        })
    else:
        if request.user.is_authenticated:
            log_security_event('no_breaches_found', request.user.pk, f"No breaches found for {email}")
        else:
            log_security_event('no_breaches_found', None, f"No breaches found for {email}")
        return JsonResponse({'message': 'No breaches found'}, status=200)

@login_required
def export_report(request) -> Union[HttpResponse, JsonResponse]:
    """
    Generate and export a report in PDF or HTML format.

    :param request: HttpRequest object.
    :return: HttpResponse or JsonResponse object.
    """
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email')
    if not validate_email(email):
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    try:
        breaches = Breach.objects.filter(user=request.user, user__email=email)
        if not breaches.exists():
            return JsonResponse({'message': 'No breaches found to export'}, status=200)

        format = request.POST.get('format', 'pdf')
        if format == 'pdf':
            report = Report.objects.create(user=request.user, report_type='pdf')
            response = generate_pdf_report(breaches)
            return HttpResponse(response, content_type='application/pdf')
        elif format == 'html':
            report = Report.objects.create(user=request.user, report_type='html')
            response = generate_html_report(breaches)
            return HttpResponse(response, content_type='text/html')
        else:
            return JsonResponse({'error': 'Unsupported format'}, status=400)

    except Exception as e:
        logger.error(f"Error exporting report: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def visualize_breaches(request) -> HttpResponse:
    """
    Generate and display a visualization of breaches.

    :param request: HttpResponse object.
    :return: HttpResponse object.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get filter parameters from request
email = request.GET.get('email', request.user.email)
if email is None:
    email = request.user.email
if email is None:
        if request.user.is_authenticated:
            log_security_event('invalid_email', request.user.pk, f"Email is None")
        else:
            log_security_event('invalid_email', None, f"Email is None")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)
    data_type = request.GET.get('data_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Use the user's email if none provided
    email = request.user.email
    if email is None:
        if request.user.is_authenticated:
            log_security_event('invalid_email', request.user.pk, f"Email is None")
        else:
            log_security_event('invalid_email', None, f"Email is None")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    email = sanitize_input(email)

    # Create visualization using the function that supports filters
    try:
        visualization = create_breach_visualization(
            user=request.user,
            data_type_filter=data_type,
            start_date=start_date,
            end_date=end_date,
            email=email
        )
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        messages.error(request, f"Error creating visualization: {str(e)}")
        return redirect('home')

    # Get unique data types for filter dropdown from database
    breaches = Breach.objects.filter(user=request.user)
    if email:
        breaches = breaches.filter(user__email=email)
    if data_type:
        breaches = breaches.filter(data_type=data_type)

    data_types = list(set(breach.data_type for breach in breaches if breach.data_type))

    context = {
        'visualization': visualization,
        'data_types': data_types,
        'current_filters': {
            'data_type': data_type,
            'start_date': start_date,
            'end_date': end_date,
            'email': email
        }
    }

    return render(request, 'leaksmap/visualization.html', context)

def register(request) -> HttpResponse:
    """
    Handle user registration.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = sanitize_input(form.cleaned_data.get('username'))
            password = sanitize_input(form.cleaned_data.get('password1'))
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful!')
                log_security_event('user_registration', user.pk, f"New user registered: {username}")
                return redirect('home')
            else:
                messages.error(request, 'Error during registration')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request) -> HttpResponse:
    """
    Handle user login.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    if request.method == 'POST':
        username = sanitize_input(request.POST.get('username'))
        password = sanitize_input(request.POST.get('password'))
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            log_security_event('user_login', user.pk, f"User logged in: {username}")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            log_security_event('login_failed', None, f"Failed login attempt for: {username}")
    return render(request, 'registration/login.html')

def user_logout(request) -> HttpResponse:
    """
    Handle user logout.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    if request.user.is_authenticated:
        log_security_event('user_logout', request.user.pk, f"User logged out: {request.user.username}")
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

@login_required
def view_profile(request) -> HttpResponse:
    """
    Display the user's profile.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    profile = request.user.userprofile
    return render(request, 'leaksmap/profile.html', {'profile': profile})

@login_required
def edit_profile(request) -> HttpResponse:
    """
    Edit the user's profile.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.birth_date = request.POST.get('birth_date', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        log_security_event('profile_updated', request.user.pk, f"Profile updated for user: {request.user.username}")
        return redirect('view_profile')

    return render(request, 'leaksmap/edit_profile.html', {'profile': profile})

@login_required
def view_report(request) -> HttpResponse:
    """
    Display the report for the user.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    report = Report.objects.filter(user=request.user).first()
    if not report:
        messages.warning(request, 'No report found for this user.')
        return redirect('home')

    return render(request, 'leaksmap/view_report.html', {'report': report})
