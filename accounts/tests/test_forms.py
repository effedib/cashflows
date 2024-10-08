from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserFormsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            team=self.User.Offices.BACKOFFICE
        )

    def test_custom_user_creation_form_valid_data(self):
        """Test CustomUserCreationForm with valid data"""
        form = CustomUserCreationForm({
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'team': self.User.Offices.FRONTOFFICE
        })
        
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.team, self.User.Offices.FRONTOFFICE)

    def test_custom_user_creation_form_invalid_data(self):
        """Test CustomUserCreationForm with invalid data"""
        form = CustomUserCreationForm({
            'username': '',  # Empty username
            'password1': 'testpass123',
            'password2': 'testpass123',
            'team': self.User.Offices.FRONTOFFICE
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_custom_user_creation_form_password_mismatch(self):
        """Test CustomUserCreationForm with mismatched passwords"""
        form = CustomUserCreationForm({
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpass',  # Different password
            'team': self.User.Offices.FRONTOFFICE
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_custom_user_creation_form_invalid_team(self):
        """Test CustomUserCreationForm with invalid team choice"""
        form = CustomUserCreationForm({
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'team': 'INVALID_TEAM'  # Invalid team choice
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('team', form.errors)

    def test_custom_user_change_form_valid_data(self):
        """Test CustomUserChangeForm with valid data"""
        form = CustomUserChangeForm(
            {
            'username': 'updateduser',
            'team': self.User.Offices.MANAGEMENT
            },
            instance=self.user)
        
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.team, self.User.Offices.MANAGEMENT)

    def test_custom_user_change_form_invalid_data(self):
        """Test CustomUserChangeForm with invalid data"""
        form = CustomUserChangeForm({
            'username': '',  # Empty username
            'team': self.User.Offices.MANAGEMENT
        }, instance=self.user)
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_fields(self):
        """Test that the forms have the correct fields"""
        creation_form = CustomUserCreationForm()
        change_form = CustomUserChangeForm()
        
        # Test CustomUserCreationForm fields
        expected_creation_fields = set(['username', 'password', 'team'])
        actual_creation_fields = set(creation_form.Meta.fields)
        self.assertEqual(actual_creation_fields, expected_creation_fields)
        
        # Test CustomUserChangeForm fields
        expected_change_fields = ['username', 'team']
        self.assertEqual(change_form.Meta.fields, expected_change_fields)

    def test_custom_user_creation_form_team_choices(self):
        """Test that the team field has the correct choices"""
        form = CustomUserCreationForm()
        team_choices = form.fields['team'].choices
        
        expected_choices = [
            ('BO', 'Back Office'),
            ('FO', 'Front Office'),
            ('PS', 'Pianificazione Strategica'),
            ('MG', 'Management'),
        ]
        
        self.assertEqual(list(team_choices), expected_choices)