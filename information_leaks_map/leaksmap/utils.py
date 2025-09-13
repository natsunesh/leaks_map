import re
from typing import List, Dict, Optional
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse

def validate_email(email: str) -> bool:
    """
    Validate the format of an email address using a regular expression.

    :param email: The email address to validate.
    :return: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_user_email() -> str:
    """
    Prompt the user to enter an email address and validate its format.

    :return: A valid email address entered by the user.
    """
    while True:
        email = input('Введите email для проверки: ').strip()

        if validate_email(email):
            return email
        else:
            print("Email некорректный, попробуйте вновь.")

def generate_pdf_report(report):
    """
    Generate a PDF report for the given report object.

    :param report: The report object to generate the PDF for.
    :return: A BytesIO object containing the PDF data.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Report for {report.email}")
    p.drawString(100, 730, f"Date: {report.created_at}")
    p.drawString(100, 710, "Breaches:")
    y = 690
    for breach in report.breach_set.all():
        p.drawString(100, y, f"- {breach.name} on {breach.date}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def generate_html_report(report):
    """
    Generate an HTML report for the given report object.

    :param report: The report object to generate the HTML for.
    :return: A string containing the HTML content.
    """
    html = f"""
    <html>
    <head><title>Report for {report.email}</title></head>
    <body>
        <h1>Report for {report.email}</h1>
        <p>Date: {report.created_at}</p>
        <h2>Breaches:</h2>
        <ul>
    """
    for breach in report.breach_set.all():
        html += f"<li>{breach.name} on {breach.date}</li>"
    html += """
        </ul>
    </body>
    </html>
    """
    return html
