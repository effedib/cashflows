from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user(self):
        """Test creating a new user"""
        user = self.User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123',
            team=self.User.Offices.FRONTOFFICE
        )
        
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.team, self.User.Offices.FRONTOFFICE)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        admin_user = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.team, self.User.Offices.BACKOFFICE)  # Default value
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_team_choices(self):
        """Test the available team choices"""
        self.assertEqual(
            self.User.Offices.choices,
            [
                ('BO', 'Back Office'),
                ('FO', 'Front Office'),
                ('PS', 'Pianificazione Strategica'),
                ('MG', 'Management'),
            ]
        )

    def test_default_team(self):
        """Test the default team value"""
        user = self.User.objects.create_user(
            username='defaultuser',
            email='default@example.com',
            password='default123'
        )
        self.assertEqual(user.team, self.User.Offices.BACKOFFICE)

    def test_change_team(self):
        """Test changing a user's team"""
        self.test_user.team = self.User.Offices.MANAGEMENT
        self.test_user.save()
        
        updated_user = self.User.objects.get(id=self.test_user.id)
        self.assertEqual(updated_user.team, self.User.Offices.MANAGEMENT)

    def test_invalid_team_choice(self):
        """Test that an invalid team choice raises an error"""
        with self.assertRaises(ValidationError):
            user = self.User.objects.create_user(
                username='invaliduser',
                email='invalid@example.com',
                password='invalid123',
                team='INVALID_CHOICE'
            )
            user.full_clean()

    def test_username_unique(self):
        """Test that username must be unique"""
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username='testuser',  # This username already exists
                email='another@example.com',
                password='pass123'
            )

    def test_email_can_be_empty(self):
        """Test that email can be empty (as per AbstractUser)"""
        user = self.User.objects.create_user(
            username='noemail',
            password='pass123'
        )
        self.assertEqual(user.email, '')