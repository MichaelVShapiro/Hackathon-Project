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

class ChatForm(forms.Form):
    """
    For handling chat info
    """
    chat_text = forms.CharField()

class UserLogInInfo(forms.Form):
    """
    For handling logging in and out functions
    """
    username = forms.CharField()
    is_logging_in = forms.BooleanField()