from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=20)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")


class PasswordResetRequestForm(forms.Form):
    channel = forms.ChoiceField(choices=[('email', 'Email'), ('whatsapp', 'WhatsApp')])
    identifier = forms.CharField(help_text="Email ou telefone (WhatsApp)")


class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password1') != cleaned.get('new_password2'):
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned