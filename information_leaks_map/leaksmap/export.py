from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.http import HttpResponse
import tempfile
import os

def generate_pdf_report(breaches):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        temp_filename = tmp.name

    p = canvas.Canvas(temp_filename, pagesize=letter)
    p.setFont("Helvetica", 12)

    y = 1000
    for breach in breaches:
        if hasattr(breach, 'service_name'):
            service_name = breach.service_name
            breach_date = breach.breach_date
            description = breach.description
        else:
            service_name = breach['service_name']
            breach_date = breach['breach_date']
            description = breach['description']

        p.drawString(100, y, f"Service: {service_name}")
        p.drawString(100, y - 20, f"Date: {breach_date}")
        p.drawString(100, y - 40, f"Description: {description}")
        y -= 60

    p.showPage()
    p.save()

    # Читаем содержимое временного файла и записываем в HttpResponse
    with open(temp_filename, 'rb') as f:
        response.write(f.read())

    # Удаляем временный файл
    os.remove(temp_filename)

    return response

def generate_html_report(breaches):
    html_content = render_to_string('leaksmap/report.html', {'breaches': breaches})
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="report.html"'
    response.write(html_content)
    return response
