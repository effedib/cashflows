from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Office


class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        self.User = get_user_model()
        self.office = Office.objects.create(name="Test Office")

    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form_invalid_data(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "",
                "email": "invalid-email",
                "password1": "testpass123",
                "password2": "differentpass",
                "team": "INVALID",
            },
        )
        self.assertEqual(response.status_code, 200)  # Rimane sulla stessa pagina
        self.assertEqual(self.User.objects.count(), 0)

    def test_signup_form_success(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "testpass123",
                "password2": "testpass123",
                "team": self.office.id,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    def test_signup_form_failure(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "",  # Invalid: empty username
                "email": "invalid-email",
                "password1": "testpass123",
                "password2": "differentpass",  # Invalid: passwords don't match
            },
        )
        self.assertEqual(response.status_code, 200)  # Form is re-displayed
        self.assertFalse(get_user_model().objects.filter(username="").exists())
