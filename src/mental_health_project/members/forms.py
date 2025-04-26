#!/usr/bin/python3
from django import forms

# this is where all form data is handled

class LogInForm(forms.Form):
    """
    The core class that stores all log in data
    """
    username = forms.CharField()
    password = forms.PasswordInput()
    remember_me = forms.BooleanField(required=False)