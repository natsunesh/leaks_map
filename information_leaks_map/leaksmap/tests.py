from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from .models import Breach
from .utils import validate_email
from .api_client import LeakCheckAPIClient
from .visualizer import create_breach_visualization
from .notifications import notify_user
from .recommendations import generate_checklist, get_security_advice
from .export import generate_pdf_report, generate_html_report
import os

class LeakCheckTests(TestCase):

    def setUp(self):
        self.email = "test@example.com"
        self.breach_data = {
            "service_name": "TestService",
            "breach_date": "2023-01-01",
            "description": "Test breach description"
        }
        self.breach = Breach.objects.create(**self.breach_data)

    def test_validate_email(self):
        self.assertTrue(validate_email(self.email))
        self.assertFalse(validate_email("invalid-email"))

    def test_check_leaks(self):
        response = self.client.post(reverse('check_leaks'), {'email': self.email})
        self.assertEqual(response.status_code, 200)
        self.assertIn('breaches', response.json())

    def test_export_report(self):
        response = self.client.post(reverse('export_report'), {'email': self.email, 'format': 'pdf'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_visualize_breaches(self):
        response = self.client.get(reverse('visualize_breaches'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaksmap/visualization.html')

    def test_notify_user(self):
        notification_message = "Test notification"
        notify_user(self.email, notification_message)
        # Add assertions to check if the notification was sent

    def test_generate_checklist(self):
        checklist = generate_checklist(self.email)
        self.assertIsInstance(checklist, list)

    def test_get_security_advice(self):
        advice = get_security_advice()
        self.assertIsInstance(advice, str)

    def test_generate_pdf_report(self):
        report = generate_pdf_report([self.breach])
        self.assertIsInstance(report, HttpResponse)
        self.assertEqual(report['Content-Type'], 'application/pdf')

    def test_generate_html_report(self):
        report = generate_html_report([self.breach])
        self.assertIsInstance(report, HttpResponse)
        self.assertEqual(report['Content-Type'], 'text/html')
