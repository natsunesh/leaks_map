from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
