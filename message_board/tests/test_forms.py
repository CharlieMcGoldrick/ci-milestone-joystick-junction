from django.test import TestCase
from django.contrib.auth import get_user_model
from message_board.forms import LoginForm, SignupForm

class LoginFormTest(TestCase):

    def setUp(self):
        # Create a user with a known username and password
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_login(self):
        # Green: Testing the form by trying the correct details
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class SignupFormTest(TestCase):

    def test_signup_form_valid(self):
        # Green: Testing the form with valid data
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123?",
            "password2": "password123?",
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())
