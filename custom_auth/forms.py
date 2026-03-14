from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'is_active', 'is_staff', 'is_superuser', 'is_verified')

    def clean_password(self):
        return self.initial["password"]