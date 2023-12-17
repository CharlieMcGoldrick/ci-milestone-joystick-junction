from django.test import TestCase
from message_board.forms import RegisterForm

class RegisterFormTest(TestCase):

    def test_register_form_valid(self):
        # Green: Testing the form with valid data
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123?",
            "password2": "password123?",
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())
