from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.http import HttpResponse

def generate_pdf_report(breaches):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    y = 1000
    for breach in breaches:
        p.drawString(100, y, f"Service: {breach.service_name}")
        p.drawString(100, y - 20, f"Date: {breach.breach_date}")
        p.drawString(100, y - 40, f"Description: {breach.description}")
        y -= 60

    p.showPage()
    p.save()
    return response

def generate_html_report(breaches):
    html_content = render_to_string('leaksmap/report.html', {'breaches': breaches})
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="report.html"'
    response.write(html_content)
    return response
