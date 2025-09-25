"""
Views for the LeaksMap application.
This module contains the view functions for handling web requests.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import validate_email
from .api_client import LeakCheckAPIClient
from .models import Breach, Report
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

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Error during registration')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

def view_profile(request):
    """
    Display the user's profile.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.userprofile
    return render(request, 'leaksmap/profile.html', {'profile': profile})

def edit_profile(request):
    """
    Edit the user's profile.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.userprofile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.birth_date = request.POST.get('birth_date', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_profile')

    return render(request, 'leaksmap/edit_profile.html', {'profile': profile})

def view_report(request):
    """
    Display the report for the user.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    report = Report.objects.filter(user=request.user).first()
    if not report:
        messages.warning(request, 'No report found for this user.')
        return redirect('home')

    return render(request, 'leaksmap/view_report.html', {'report': report})
