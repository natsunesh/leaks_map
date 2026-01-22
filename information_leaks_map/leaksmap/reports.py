
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Report, Breach
from .export import generate_pdf_report, generate_html_report

@login_required
def generate_report(request):
    """
    Generate a report based on user input.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        format = request.POST.get('format', 'pdf')

        if not email:
            messages.error(request, 'Email is required')
            return redirect('generate_report')

        # Get breaches for the email (user is authenticated due to @login_required)
        breaches = Breach.objects.filter(user=request.user, user__email=email)

        if not breaches.exists():
            messages.warning(request, 'No breaches found for this email')
            return redirect('generate_report')

        # Create report
        report = Report.objects.create(
            user=request.user,
            email=email
        )

        # Add breaches to the report
        for breach in breaches:
            breach.report = report
            breach.save()

        

    return render(request, 'leaksmap/generate_report.html')

@login_required
def view_report(request, report_id):
    """
    View a specific report by ID.
    """
    try:
        report = Report.objects.get(id=report_id, user=request.user)
        return render(request, 'leaksmap/view_report.html', {'report': report})
    except Report.DoesNotExist:
        messages.error(request, 'Report not found')
        return redirect('home')

@login_required
def export_report(request, report_id):
    """
    Export a specific report.
    """
    try:
        report = Report.objects.get(id=report_id, user=request.user)
        # Get breaches for the report
        if report.email:
            breaches = Breach.objects.filter(user=request.user, user__email=report.email)
        else:
            breaches = Breach.objects.filter(user=request.user)
        
        if not breaches.exists():
            messages.warning(request, 'No breaches found for this report')
            return redirect('view_report', report_id=report_id)
        
        response = generate_pdf_report(breaches)
        return response
    except Report.DoesNotExist:
        messages.error(request, 'Report not found')
        return redirect('home')
