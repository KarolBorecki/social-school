import random
import string

from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordResetForm(forms.Form):
    email = forms.CharField(required=True, label='Email')

    @staticmethod
    def generate_new_pass(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for i in range(size))
