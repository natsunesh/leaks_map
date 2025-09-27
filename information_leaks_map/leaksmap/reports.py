"""
Report generation module for creating and viewing reports.
"""

from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib import messages
from .models import Report, Breach
from .export import generate_pdf_report, generate_html_report

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

        # Get breaches for the email
        breaches = Breach.objects.filter(email=email)

        if not breaches.exists():
            messages.warning(request, 'No breaches found for this email')
            return redirect('generate_report')

        # Create report
        report = Report.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email
        )

        # Generate report in requested format
        if format == 'pdf':
            pdf_file = generate_pdf_report(report)
            return FileResponse(pdf_file, filename=f'report_{email}.pdf')
        else:
            html_content = generate_html_report(report)
            return FileResponse(html_content, filename=f'report_{email}.html')

    return render(request, 'leaksmap/generate_report.html')

def view_report(request, report_id):
    """
    View a specific report by ID.
    """
    try:
        report = Report.objects.get(id=report_id)
        return render(request, 'leaksmap/view_report.html', {'report': report})
    except Report.DoesNotExist:
        messages.error(request, 'Report not found')
        return redirect('home')
