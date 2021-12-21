# users/tests/test_views.py
from django import forms
from django.test import TestCase
from django.urls import reverse


class UserSignUpViewTest(TestCase):
    def test_signup_page_correct_context(self):
        response = self.client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
