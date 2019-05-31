from django.forms import CharField, PasswordInput, Form
from django import forms

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())