from django.test import TestCase
from django.contrib.auth import get_user_model
from message_board.forms import LoginForm, SignupForm

class LoginFormTest(TestCase):

    def test_nonexistent_username(self):
        # Red: Testing the form by trying a user with a different username
        User = get_user_model()
        User.objects.create_user(username='existing_user', password='testpassword')

        form_data = {
            'username': 'nonexistent_user',
            'password': 'testpassword',
        }

        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


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
