from django.shortcuts import render
from django.http import FileResponse
from .models import Report
from .utils import generate_pdf_report

def generate_report(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        report = Report.objects.create(user=request.user, email=email)
        pdf_file = generate_pdf_report(report)
        return FileResponse(pdf_file, filename='report.pdf')
    return render(request, 'leaksmap/generate_report.html')

def view_report(request, report_id):
    try:
        report = Report.objects.get(id=report_id, user=request.user)
        return render(request, 'leaksmap/view_report.html', {'report': report})
    except Report.DoesNotExist:
        return render(request, 'leaksmap/home.html', {'error': 'Report not found'})
