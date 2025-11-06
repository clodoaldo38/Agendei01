from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
import random

from .forms import SignupForm, PasswordResetRequestForm, CodeVerificationForm
from .models import UserProfile, VerificationCode


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        user = form.save()
        user.email = form.cleaned_data['email']
        user.save(update_fields=['email'])
        phone = form.cleaned_data.get('phone')
        UserProfile.objects.create(user=user, phone=phone or '')
        login(self.request, user)
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home')


class PasswordResetRequestView(FormView):
    template_name = 'accounts/password_reset_request.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('verify_code')

    def form_valid(self, form):
        channel = form.cleaned_data['channel']
        identifier = form.cleaned_data['identifier']
        user = None
        if channel == 'email':
            try:
                user = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                form.add_error('identifier', 'Email não encontrado.')
                return self.form_invalid(form)
        else:
            try:
                user = UserProfile.objects.select_related('user').get(phone=identifier).user
            except UserProfile.DoesNotExist:
                form.add_error('identifier', 'Telefone não encontrado.')
                return self.form_invalid(form)

        code = f"{random.randint(100000, 999999)}"
        VerificationCode.objects.create(
            user=user,
            code=code,
            channel=channel,
            purpose='password_reset',
            expires_at=VerificationCode.generate_expiry(10)
        )

        if channel == 'email':
            send_mail(
                subject='Código de verificação (Agendei)',
                message=f'Seu código é: {code}',
                from_email='no-reply@agendei.local',
                recipient_list=[user.email],
            )
        else:
            # Stub de envio WhatsApp: em produção, integrar Twilio/Meta API
            print(f"[WHATSAPP] Enviar para {identifier}: código {code}")

        # Armazenar em sessão para facilitar
        self.request.session['password_reset_user_id'] = user.id
        self.request.session['password_reset_channel'] = channel
        return super().form_valid(form)


class CodeVerifyView(FormView):
    template_name = 'accounts/code_verify.html'
    form_class = CodeVerificationForm
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        user_id = self.request.session.get('password_reset_user_id')
        if not user_id:
            form.add_error(None, 'Sessão expirada. Solicite novo código.')
            return self.form_invalid(form)
        code = form.cleaned_data['code']
        try:
            vc = VerificationCode.objects.filter(user_id=user_id, purpose='password_reset', used=False).latest('created_at')
        except VerificationCode.DoesNotExist:
            form.add_error('code', 'Código inválido ou expirado.')
            return self.form_invalid(form)

        if vc.code != code:
            form.add_error('code', 'Código incorreto.')
            return self.form_invalid(form)
        if timezone.now() > vc.expires_at:
            form.add_error('code', 'Código expirado. Solicite outro.')
            return self.form_invalid(form)

        new_password = form.cleaned_data['new_password1']
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        vc.mark_used()
        login(self.request, user)
        # Limpar sessão
        for k in ('password_reset_user_id', 'password_reset_channel'):
            self.request.session.pop(k, None)
        return super().form_valid(form)


# Create your views here.
