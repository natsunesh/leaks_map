from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Breach

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.breach = Breach.objects.create(
            user=self.user,
            service_name='Test Service',
            breach_date='2023-01-01',
            description='Test breach'
        )

    def test_get_security_advice(self):
        self.client.login(username='testuser', password='password')
        breaches = Breach.objects.all()
        response = self.client.get(reverse('get_security_advice'), {'breaches': list(breaches)})
        self.assertEqual(response.status_code, 200)
        self.assertIn('advice', response.json())

    def test_generate_service_security_advice(self):
        self.client.login(username='testuser', password='password')
        breaches = Breach.objects.all()
        response = self.client.get(reverse('generate_service_security_advice'), {'breaches': list(breaches)})
        self.assertEqual(response.status_code, 200)
        self.assertIn('advice', response.json())

    def test_generate_security_advice_for_breach(self):
        self.client.login(username='testuser', password='password')
        breach = Breach.objects.first()
        response = self.client.get(reverse('generate_security_advice_for_breach'), {'breach': breach})
        self.assertEqual(response.status_code, 200)
        self.assertIn('advice', response.json())

    def test_check_leaks(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('check_leaks'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_user_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_user_login(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_edit_profile(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('edit_profile'), {
            'bio': 'New bio',
            'location': 'New location'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_view_profile(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_visualize_breaches(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('visualize_breaches'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_home(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

    def test_chronological_journal(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('chronological_journal'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())

def test_help_page(self) -> None:
    self.client.login(username='testuser', password='password')
    response = self.client.get(reverse('help_page'))
    self.assertEqual(response.status_code, 200)
    self.assertIn('status', response.json())
