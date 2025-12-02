from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Breach
from .views import get_security_advice, generate_service_security_advice, generate_security_advice_for_breach

class SecurityAdviceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.breach1 = Breach.objects.create(
            service_name="ExampleService",
            breach_date="2023-01-01",
            data_type="Password",
            description="Test breach",
            user=self.user  # ИСПРАВЛЕНО: добавлен пользователь для связи с Breach
        )
        self.breach2 = Breach.objects.create(
            service_name="ExampleService",
            breach_date="2023-02-01",
            data_type="Email",
            description="Another test breach",
            user=self.user  # ИСПРАВЛЕНО: добавлен пользователь для связи с Breach
        )

    def test_get_security_advice(self):
        self.client.login(username='testuser', password='testpassword')
        breaches = [self.breach1, self.breach2]
        response = self.client.post(reverse('get_security_advice'), {'breaches': breaches})  # ИСПРАВЛЕНО: использование POST вместо GET
        self.assertEqual(response.status_code, 200)
        self.assertIn("Change your password for ExampleService", response.content.decode())
        self.assertIn("Check your Email for any suspicious activity", response.content.decode())

    def test_generate_service_security_advice(self):
        breaches = [self.breach1, self.breach2]
        advice = generate_service_security_advice(breaches)
        self.assertIn("Change your password for ExampleService", advice.content.decode())
        self.assertIn("Check your Email for any suspicious activity", advice.content.decode())

    def test_generate_security_advice_for_breach(self):
        advice = generate_security_advice_for_breach(self.breach1)
        self.assertIn("Change your password for ExampleService", advice.content.decode())
        self.assertIn("Check your Password for any suspicious activity", advice.content.decode())
