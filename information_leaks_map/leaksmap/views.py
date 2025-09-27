"""
Views for the LeaksMap application.
This module contains the view functions for handling web requests.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any, List, Union
from .utils import validate_email, sanitize_input, log_security_event
from .api_client import LeakCheckAPIClient
from .models import Breach, Report, UserProfile
from .export import generate_pdf_report, generate_html_report
from .visualizer import create_breach_visualization
import os
import logging

logger = logging.getLogger(__name__)

def home(request) -> HttpResponse:
    """
    Render the home page.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    return render(request, 'leaksmap/home.html')

@login_required
def check_leaks(request) -> JsonResponse:
    """
    Check for data breaches associated with a given email address.

    :param request: HttpRequest object.
    :return: JsonResponse object.
    """
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email')
    if not validate_email(email):
        return JsonResponse({'error': 'Invalid email address'}, status=400)

    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API key not configured")
        return JsonResponse({'error': 'API key not configured'}, status=500)

    try:
        api_client = LeakCheckAPIClient(api_key=api_key)
    except Exception as e:
        logger.error(f"Error initializing API client: {str(e)}")
        return JsonResponse({'error': f"Error initializing API client: {str(e)}"}, status=500)
    try:
        breaches = api_client.get_breach_info(email)
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return JsonResponse({'error': f"API error: {str(e)}"}, status=500)

    if breaches:
        # Save breaches to database
        for breach in breaches:
            try:
                Breach.objects.create(
                    user=request.user,
                    service_name=breach.get('service_name', 'Unknown'),
                    breach_date=breach.get('breach_date', '2000-01-01'),
                    description=breach.get('description', 'No description'),
                    source=breach.get('source', 'Unknown')
                )
            except ValidationError as e:
                logger.error(f"Validation error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=400)

        log_security_event('data_breach_found', request.user.id, f"Found {len(breaches)} breaches for {email}")
        return JsonResponse({
            'breaches': breaches,
            'message': 'Breaches found'
        })
    else:
        log_security_event('no_breaches_found', request.user.id, f"No breaches found for {email}")
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
        return JsonResponse({'error': 'Invalid email address'}, status=400)

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
    data_type = request.GET.get('data_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Create visualization with filters
    try:
        visualization = create_breach_visualization(
            request.user,
            data_type_filter=data_type,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        messages.error(request, f"Error creating visualization: {str(e)}")
        return redirect('home')

    # Get unique data types for filter dropdown
    try:
        data_types = Breach.objects.filter(user=request.user).values_list('data_type', flat=True).distinct()
    except Exception as e:
        logger.error(f"Error fetching data types: {str(e)}")
        messages.error(request, f"Error fetching data types: {str(e)}")
        return redirect('home')

    context = {
        'visualization': visualization,
        'data_types': data_types,
        'current_filters': {
            'data_type': data_type,
            'start_date': start_date,
            'end_date': end_date
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
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
        username = request.POST.get('username')
        password = request.POST.get('password')
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
        log_security_event('user_logout', request.user.id, f"User logged out: {request.user.username}")
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
        profile.bio = sanitize_input(request.POST.get('bio', ''))
        profile.location = sanitize_input(request.POST.get('location', ''))
        profile.birth_date = request.POST.get('birth_date', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        log_security_event('profile_updated', request.user.id, f"Profile updated for user: {request.user.username}")
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
