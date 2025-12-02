import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
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
from .notifications import notify_user
from .recommendations import generate_checklist, get_security_advice
from .rate_limit import rate_limit

from dateutil.parser import parse as date_parser
import os
import logging
import asyncio
import re
from datetime import datetime

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
    if request.method not in ['GET', 'POST']:
        log_security_event('invalid_request_method', request.user.pk if request.user.is_authenticated else None, f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email', request.user.email)
    if email is None:
        log_security_event('invalid_email', request.user.pk if request.user.is_authenticated else None, f"Email is None")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    email = sanitize_input(email)
    if not validate_email(email):
        log_security_event('invalid_email', request.user.pk if request.user.is_authenticated else None, f"Invalid email format: {email}")
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    all_breaches = []
    api_errors = []

    # LeakCheck API
    leakcheck_api_key: Optional[str] = os.getenv("API_KEY")
    if leakcheck_api_key:
        leakcheck_api_key = leakcheck_api_key.strip()
        try:
            leakcheck_client = LeakCheckAPIClient(api_key=leakcheck_api_key)
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, use asyncio.run which creates a new event loop
                    leakcheck_breaches = asyncio.run(leakcheck_client._fetch_data_leakcheck(email)) or []
                else:
                    leakcheck_breaches = loop.run_until_complete(leakcheck_client._fetch_data_leakcheck(email)) or []
            except RuntimeError:
                # No event loop, create a new one
                leakcheck_breaches = asyncio.run(leakcheck_client._fetch_data_leakcheck(email)) or []
            all_breaches.extend(leakcheck_breaches)
        except Exception as e:
            logger.error(f"LeakCheck API error: {e}")
            api_errors.append(f"LeakCheck API error: {str(e)}")

    # Have I Been Pwned API
    hibp_api_key: Optional[str] = os.getenv("HIBP_API_KEY")
    if hibp_api_key:
        hibp_api_key = hibp_api_key.strip()
        try:
            hibp_client = HaveIBeenPwnedAPIClient(api_key=hibp_api_key)
            hibp_breaches = hibp_client.get_breach_info_hibp(email) or []
            all_breaches.extend(hibp_breaches)
        except Exception as e:
            logger.error(f"Have I Been Pwned API error: {e}")
            api_errors.append(f"Have I Been Pwned API error: {str(e)}")
    
    # If both APIs failed, return error
    if api_errors and not all_breaches:
        return JsonResponse({'error': '; '.join(api_errors)}, status=500)

    if all_breaches:
        # Save breaches to database
        saved_count = 0
        for breach in all_breaches:
            try:
                # Handle date format from API (YYYY-MM)
                breach_date = breach.get('breach_date', '2000-01-01')
                if breach_date and isinstance(breach_date, str):
                    if re.match(r'^\d{4}-\d{2}$', breach_date):
                        try:
                            breach_date = date_parser(breach_date).strftime('%Y-%m-%d')
                        except ValueError:
                            logger.error(f"Invalid date format: {breach_date}, using default")
                            breach_date = '2000-01-01'
                    elif not re.match(r'^\d{4}-\d{2}-\d{2}$', breach_date):
                        logger.warning(f"Unexpected date format: {breach_date}, using default")
                        breach_date = '2000-01-01'

                # Ensure all required fields are present
                service_name = breach.get('service_name', 'Unknown')
                description = breach.get('description', 'No description')
                source = breach.get('source', 'Unknown')
                data_type = breach.get('data_type', 'Unknown')
                location = breach.get('location', 'Unknown')

                # Create or update breach record
                breach_obj, created = Breach.objects.get_or_create(
                    user=request.user,
                    service_name=service_name,
                    breach_date=breach_date,
                    defaults={
                        'description': description,
                        'source': source,
                        'data_type': data_type,
                        'location': location,
                    }
                )
                if created:
                    saved_count += 1
            except ValidationError as e:
                logger.error(f"Validation error for breach {breach.get('service_name', 'Unknown')}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error saving breach {breach.get('service_name', 'Unknown')}: {str(e)}")
                continue

        log_security_event('data_breach_found', request.user.pk if request.user.is_authenticated else None, f"Found {len(all_breaches)} breaches for {email}, saved {saved_count}")
        
        # Send notifications if new breaches were found
        if saved_count > 0:
            try:
                message = f"Обнаружено {saved_count} новых утечек данных для вашего email: {email}"
                notification_results = notify_user(
                    user=request.user,
                    message=message,
                    subject='Обнаружены новые утечки данных',
                    breach_details=all_breaches[:saved_count] if saved_count <= len(all_breaches) else all_breaches
                )
                logger.info(f"Notification results: {notification_results}")
            except Exception as e:
                logger.error(f"Failed to send notifications: {str(e)}")
        
        response_data = {
            'breaches': all_breaches,
            'message': 'Breaches found',
            'redirect_url': f'/visualize_breaches/?email={email}'
        }
        if api_errors:
            response_data['warnings'] = api_errors
        return JsonResponse(response_data)
    else:
        log_security_event('no_breaches_found', request.user.pk if request.user.is_authenticated else None, f"No breaches found for {email}")
        return JsonResponse({'message': 'No breaches found'}, status=200)

@login_required
def export_report(request) -> Union[HttpResponse, JsonResponse]:
    """
    Generate and export a report in PDF or HTML format.

    :param request: HttpRequest object.
    :return: HttpResponse or JsonResponse object.
    """
    if request.method not in ['GET', 'POST']:
        log_security_event('invalid_request_method', request.user.pk, f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email')
    if not validate_email(email):
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    try:
        # Filter breaches by user and email
        breaches = Breach.objects.filter(user=request.user)
        if email and email != request.user.email:
            # If email is provided and different from user's email, filter by it
            breaches = breaches.filter(user__email=email)
        
        if not breaches.exists():
            return JsonResponse({'message': 'No breaches found to export'}, status=200)

        format = request.POST.get('format', 'pdf').lower()
        if format == 'pdf':
            report = Report.objects.create(user=request.user, report_type='pdf', email=email)
            response = generate_pdf_report(breaches)
            return response
        elif format == 'html':
            report = Report.objects.create(user=request.user, report_type='html', email=email)
            response = generate_html_report(breaches)
            return response
        else:
            return JsonResponse({'error': 'Unsupported format'}, status=400)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'Unexpected error'}, status=500)

@login_required
def visualize_breaches(request) -> HttpResponse:
    """
    Generate and display a visualization of breaches.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    if request.method not in ['GET', 'POST']:
        log_security_event('invalid_request_method', request.user.pk, f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    email = request.POST.get('email') if request.method == 'POST' else request.GET.get('email')
    # If email is not provided, use user's email
    if not email:
        email = request.user.email if request.user.is_authenticated else None
    
    if email and not validate_email(email):
        return JsonResponse({'error': 'Invalid email address.'}, status=400)

    # Create visualization using the function that supports filters
    try:
        visualization = create_breach_visualization(
            user=request.user,
            data_type_filter=request.GET.get('data_type'),
            start_date=request.GET.get('start_date'),
            end_date=request.GET.get('end_date'),
            email=email
        )
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        messages.error(request, f"Error creating visualization: {str(e)}")
        return redirect('home')

    # Get unique data types for filter dropdown from database
    breaches = Breach.objects.filter(user=request.user)
    if email and email != request.user.email:
        breaches = breaches.filter(user__email=email)
    data_types = list(set(breach.data_type for breach in breaches if breach.data_type) if breaches.exists() else [])

    context = {
        'visualization': visualization,
        'data_types': data_types,
        'current_filters': {
            'data_type': request.GET.get('data_type'),
            'start_date': request.GET.get('start_date'),
            'end_date': request.GET.get('end_date'),
            'email': email
        }
    }

    return render(request, 'leaksmap/visualization.html', context)

def register(request) -> Union[HttpResponse, JsonResponse]:
    """
    Handle user registration.

    :param request: HttpRequest object.
    :return: HttpResponse or JsonResponse object.
    """
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = sanitize_input(form.cleaned_data.get('username'))
            password = form.cleaned_data.get('password1')  # Don't sanitize password
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful!')
                log_security_event('user_registration', user.pk, f"New user registered: {username}")
                return redirect('home')
            else:
                messages.error(request, 'Error during registration')
                return render(request, 'registration/register.html', {'form': form, 'error': 'Error during registration'})
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@rate_limit(max_attempts=5, window=300)  # 5 попыток за 5 минут
def user_login(request) -> Union[HttpResponse, JsonResponse]:
    """
    Handle user login with rate limiting protection.

    :param request: HttpRequest object.
    :return: HttpResponse or JsonResponse object.
    """
    # Get IP for logging
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    elif request.method == 'POST':
        username = sanitize_input(request.POST.get('username', ''))
        password = request.POST.get('password', '')  # Don't sanitize password
        if not username or not password:
            messages.error(request, 'Username and password are required')
            log_security_event('login_failed', None, f"Empty credentials from IP: {ip}")
            return render(request, 'registration/login.html', {'error': 'Username and password are required'})
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            log_security_event('user_login', user.pk, f"User logged in: {username} from IP: {ip}")
            logger.info(f"Successful login: {username} from IP: {ip}")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            log_security_event('login_failed', None, f"Failed login attempt for: {username} from IP: {ip}")
            logger.warning(f"Failed login attempt: {username} from IP: {ip}")
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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
    # Ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'leaksmap/profile.html', {'profile': profile})

@login_required
def edit_profile(request) -> HttpResponse:
    """
    Edit the user's profile.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    if request.method == 'GET':
        # Ensure profile exists
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'leaksmap/edit_profile.html', {'profile': profile})
    elif request.method == 'POST':
        # Ensure profile exists
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.POST.get('birth_date'):
            profile.birth_date = request.POST.get('birth_date')
        if request.POST.get('bio'):
            # Sanitize bio to prevent XSS
            profile.bio = sanitize_input(request.POST.get('bio'))
        if request.POST.get('location'):
            # Sanitize location to prevent XSS
            profile.location = sanitize_input(request.POST.get('location'))
        if request.POST.get('telegram_id'):
            # Sanitize telegram_id to prevent XSS
            profile.telegram_id = sanitize_input(request.POST.get('telegram_id'))
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        log_security_event('profile_updated', request.user.pk, f"Profile updated for user: {request.user.username}")
        return redirect('view_profile')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# view_report is now in reports.py to avoid conflicts

@login_required
def chronological_journal(request) -> HttpResponse:
    """
    Display a chronological journal of breaches with filtering options.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    # Get all breaches for the user
    breaches = Breach.objects.filter(user=request.user).order_by('-breach_date')
    
    # Apply filters
    email_filter = request.GET.get('email')
    if email_filter:
        breaches = breaches.filter(user__email=email_filter)
    else:
        breaches = breaches.filter(user__email=request.user.email)
    
    data_type_filter = request.GET.get('data_type')
    if data_type_filter:
        breaches = breaches.filter(data_type=data_type_filter)
    
    service_filter = request.GET.get('service')
    if service_filter:
        breaches = breaches.filter(service_name__icontains=service_filter)
    
    start_date = request.GET.get('start_date')
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            breaches = breaches.filter(breach_date__gte=start_dt)
        except ValueError:
            logger.warning(f"Invalid start_date format: {start_date}")
    
    end_date = request.GET.get('end_date')
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            breaches = breaches.filter(breach_date__lte=end_dt)
        except ValueError:
            logger.warning(f"Invalid end_date format: {end_date}")
    
    # Get unique values for filter dropdowns
    all_user_breaches = Breach.objects.filter(user=request.user)
    data_types = sorted(set(b.data_type for b in all_user_breaches if b.data_type))
    services = sorted(set(b.service_name for b in all_user_breaches))
    
    context = {
        'breaches': breaches,
        'data_types': data_types,
        'services': services,
        'current_filters': {
            'email': email_filter or request.user.email,
            'data_type': data_type_filter,
            'service': service_filter,
            'start_date': start_date,
            'end_date': end_date,
        }
    }
    
    return render(request, 'leaksmap/chronological_journal.html', context)

@login_required
def help_page(request) -> HttpResponse:
    """
    Display help page with recommendations and security advice.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    # Get user's breaches for personalized recommendations
    breaches = Breach.objects.filter(user=request.user)
    
    # Generate checklist and advice
    breach_list = [{
        'service_name': b.service_name,
        'breach_date': b.breach_date,
        'data_type': b.data_type,
        'description': b.description
    } for b in breaches]
    
    checklist = generate_checklist(breach_list)
    security_advice = get_security_advice(breaches)
    
    # Group breaches by service for service-specific checklists
    service_breaches = {}
    for breach in breaches:
        service = breach.service_name
        if service not in service_breaches:
            service_breaches[service] = []
        service_breaches[service].append(breach)
    
    # Generate service-specific checklists
    service_checklists = {}
    for service, service_breach_list in service_breaches.items():
        service_checklists[service] = generate_checklist([{
            'service_name': b.service_name,
            'breach_date': b.breach_date,
            'data_type': b.data_type,
            'description': b.description
        } for b in service_breach_list])
    
    context = {
        'checklist': checklist,
        'security_advice': security_advice,
        'service_checklists': service_checklists,
        'breach_count': breaches.count(),
    }
    
    return render(request, 'leaksmap/help.html', context)
