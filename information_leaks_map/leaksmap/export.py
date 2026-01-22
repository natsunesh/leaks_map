from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.http import HttpResponse
import tempfile
import os
import logging
from .recommendations import generate_checklist, get_security_advice

logger = logging.getLogger(__name__)



def generate_pdf_report(breaches):
    """
    Generate a PDF report from breaches.
    
    :param breaches: QuerySet or list of Breach objects
    :return: HttpResponse with PDF content
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    temp_filename = None
    try:
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            temp_filename = tmp.name

        p = canvas.Canvas(temp_filename, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        
        # Title
        p.drawString(100, 1000, "Отчет об утечках данных")
        y = 970
        p.setFont("Helvetica", 12)

        page_height = 100
        breach_count = 0
        
        # Breaches section
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Обнаруженные утечки:")
        y -= 30
        p.setFont("Helvetica", 12)
        
        # Convert breaches to list for recommendations
        breach_list = []
        for breach in breaches:
            if y < page_height:
                p.showPage()
                y = 1000
            
            if hasattr(breach, 'service_name'):
                service_name = str(breach.service_name)
                breach_date = str(breach.breach_date)
                description = str(breach.description)[:100]  # Limit description length
                data_type = str(breach.data_type) if breach.data_type else "Не указан"
                breach_list.append({
                    'service_name': service_name,
                    'breach_date': breach_date,
                    'data_type': data_type,
                    'description': description
                })
            else:
                service_name = str(breach.get('service_name', 'Unknown'))
                breach_date = str(breach.get('breach_date', 'Unknown'))
                description = str(breach.get('description', 'No description'))[:100]
                data_type = str(breach.get('data_type', 'Не указан'))
                breach_list.append({
                    'service_name': service_name,
                    'breach_date': breach_date,
                    'data_type': data_type,
                    'description': description
                })

            p.drawString(100, y, f"Сервис: {service_name}")
            p.drawString(100, y - 20, f"Дата: {breach_date}")
            p.drawString(100, y - 40, f"Тип данных: {data_type}")
            p.drawString(100, y - 60, f"Описание: {description}")
            y -= 90
            breach_count += 1

        if breach_count == 0:
            p.drawString(100, y, "Утечек не найдено")
        else:
            # Add recommendations section
            if y < page_height + 200:
                p.showPage()
                y = 1000
            
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y, "Рекомендации по устранению угроз:")
            y -= 30
            p.setFont("Helvetica", 12)
            
            # Generate recommendations
            checklist = generate_checklist(breach_list)
            for item in checklist:
                if y < page_height:
                    p.showPage()
                    y = 1000
                p.drawString(120, y, f"• {item}")
                y -= 25
            
            # Add security advice
            if y < page_height + 100:
                p.showPage()
                y = 1000
            
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y, "Общие рекомендации по безопасности:")
            y -= 30
            p.setFont("Helvetica", 12)
            
            security_advice = get_security_advice(breaches)
            advice_lines = security_advice.split('\n')
            for line in advice_lines:
                if line.strip():
                    if y < page_height:
                        p.showPage()
                        y = 1000
                    p.drawString(120, y, line.strip())
                    y -= 20

        p.showPage()
        p.save()

        # Читаем содержимое временного файла и записываем в HttpResponse
        with open(temp_filename, 'rb') as f:
            response.write(f.read())

    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        response = HttpResponse(content_type='text/plain')
        response.write(f"Error generating report: {str(e)}")
    finally:
        # Удаляем временный файл
        if temp_filename and os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")

    return response

def generate_html_report(breaches):
    """
    Generate an HTML report from breaches with recommendations.
    
    :param breaches: QuerySet or list of Breach objects
    :return: HttpResponse with HTML content
    """
    try:
        # Convert breaches to list for recommendations
        breach_list = []
        for breach in breaches:
            if hasattr(breach, 'service_name'):
                breach_list.append({
                    'service_name': breach.service_name,
                    'breach_date': breach.breach_date,
                    'data_type': breach.data_type,
                    'description': breach.description
                })
            else:
                breach_list.append({
                    'service_name': breach.get('service_name', 'Unknown'),
                    'breach_date': breach.get('breach_date', 'Unknown'),
                    'data_type': breach.get('data_type', 'Не указан'),
                    'description': breach.get('description', 'No description')
                })
        
        # Generate recommendations
        checklist = generate_checklist(breach_list)
        security_advice = get_security_advice(breaches)
        
        context = {
            'breaches': breaches,
            'checklist': checklist,
            'security_advice': security_advice
        }
        
        html_content = render_to_string('leaksmap/report.html', context)
        response = HttpResponse(content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="report.html"'
        response.write(html_content)
        return response
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        response = HttpResponse(content_type='text/plain')
        response.write(f"Error generating report: {str(e)}")
        return response
