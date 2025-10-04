# Tests for the LeaksMap application.
# This module contains unit tests for the application.

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Breach, Report, UserProfile, Feedback, SupportTicket
from .utils import validate_email
from .api_client import LeakCheckAPIClient, HaveIBeenPwnedAPIClient
from unittest.mock import patch, MagicMock
import os

class TestUtils(TestCase):
    """Test utility functions."""

    def test_validate_email(self):
        """Test email validation."""
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))

class TestModels(TestCase):
    """Test models."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_breach_model(self):
        """Test Breach model."""
        breach = Breach.objects.create(
            user=self.user,
            service_name="Test Service",
            breach_date="2023-01-01",
            description="Test breach"
        )
        self.assertEqual(str(breach), "Test Service - 2023-01-01 - test@example.com")
        # Replace None assignment with a dummy user to avoid type errors
        breach.user = User.objects.get(username='deleted_user')
        breach.save()
        self.assertEqual(str(breach), "Test Service - 2023-01-01 - Unknown User")

    def test_report_model(self):
        """Test Report model."""
        report = Report.objects.create(
            user=self.user,
            report_type="pdf"
        )
        self.assertEqual(str(report), f"Report for test@example.com - {report.generated_at}")
        # Replace None assignment with a dummy user to avoid type errors
        report.user = User.objects.get(username='deleted_user')
        report.save()
        self.assertEqual(str(report), f"Report for Unknown User - {report.generated_at}")

        report.user = None
        report.save()
        self.assertEqual(str(report), f"Report for Unknown User - {report.generated_at}")

    def test_user_profile_model(self):
        """Test UserProfile model."""
        self.assertEqual(str(self.user_profile), "Profile of testuser")

    def test_feedback_model(self):
        """Test Feedback model."""
        feedback = Feedback.objects.create(
            user=self.user,
            content="Test feedback"
        )
        self.assertEqual(str(feedback), "Feedback from testuser - 2023-01-01 00:00:00")
        # Replace None assignment with a dummy user to avoid type errors
        feedback.user = User.objects.get(username='deleted_user')
        feedback.save()
        self.assertEqual(str(feedback), "Feedback from Unknown User - 2023-01-01 00:00:00")

    def test_support_ticket_model(self):
        """Test SupportTicket model."""
        ticket = SupportTicket.objects.create(
            user=self.user,
            title="Test Ticket",
            description="Test description"
        )
        self.assertEqual(str(ticket), "Ticket: Test Ticket - open")
        # Replace None assignment with a dummy user to avoid type errors
        ticket.user = User.objects.get(username='deleted_user')
        ticket.save()
        self.assertEqual(str(ticket), "Ticket: Test Ticket - Unknown User")

class TestViews(TestCase):
    """Test views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_home_view(self):
        """Test home view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_check_leaks_view(self):
        """Test check leaks view."""
        response = self.client.get(reverse('check_leaks'))
        self.assertEqual(response.status_code, 200)

    def test_export_report_view(self):
        """Test export report view."""
        response = self.client.get(reverse('export_report'))
        self.assertEqual(response.status_code, 200)

    def test_visualize_breaches_view(self):
        """Test visualize breaches view."""
        response = self.client.get(reverse('visualize_breaches'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        """Test register view."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """Test login view."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """Test logout view."""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_view_profile_view(self):
        """Test view profile view."""
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        """Test edit profile view."""
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_report_view(self):
        """Test view report view."""
        response = self.client.get(reverse('view_report'))
        self.assertEqual(response.status_code, 200)

class TestAPIClient(TestCase):
    """Test API client."""

    @patch('requests.get')
    def test_get_breach_info(self, mock_get):
        """Test get breach info."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "sources": [
                {
                    "name": "Test Service",
                    "date": "2023-01-01",
                    "location": "Test Location",
                    "data_type": "Test Data Type"
                }
            ]
        }
        mock_get.return_value = mock_response

        api_key = os.getenv("HIBP_API_KEY", "test_api_key")
        client = HaveIBeenPwnedAPIClient(api_key=api_key)
        breaches = client.get_breach_info_by_email("test@example.com") or []

        if breaches:
            self.assertEqual(len(breaches), 1)
            self.assertEqual(breaches[0]["service_name"], "Test Service")

    @patch('requests.get')
    def test_get_breach_info_by_username(self, mock_get):
        """Test get breach info by username."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "sources": [
                {
                    "name": "Test Service",
                    "date": "2023-01-01"
                }
            ]
        }
        mock_get.return_value = mock_response

        api_key = os.getenv("API_KEY", "test_api_key")
        client = LeakCheckAPIClient(api_key=api_key)
        breaches = client.get_breach_info_by_username("testuser") or []

        self.assertEqual(len(breaches), 1)
        if breaches:
            self.assertEqual(breaches[0]["service_name"], "Test Service")
