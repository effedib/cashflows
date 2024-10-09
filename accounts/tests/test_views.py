from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.User = get_user_model()

    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'team': 'BO'
        })
        self.assertEqual(response.status_code, 302)  # Redirect dopo il successo
        self.assertEqual(self.User.objects.count(), 1)
        new_user = self.User.objects.first()
        self.assertEqual(new_user.username, 'testuser')
        self.assertEqual(new_user.team, 'BO')

    def test_signup_form_invalid_data(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'team': 'INVALID'
        })
        self.assertEqual(response.status_code, 200)  # Rimane sulla stessa pagina
        self.assertEqual(self.User.objects.count(), 0)