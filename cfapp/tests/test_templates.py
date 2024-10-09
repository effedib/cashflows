from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class BaseTemplateTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_template_rendering(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Change password')
        self.assertContains(response, 'testuser')

    def test_unauthenticated_user(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Log in')
        self.assertContains(response, 'Sign up')


class HomeTemplateTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_template_rendering(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_authenticated_user_content(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Visualizza incassi')
        self.assertNotContains(response, 'Log in')

    def test_unauthenticated_user_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Log in')
        self.assertNotContains(response, 'Visualizza incassi')


class LoginTemplateTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_template_rendering(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_form_display(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'Log In')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inserisci nome utente e password corretti. In entrambi i campi le maiuscole potrebbero essere significative.')
