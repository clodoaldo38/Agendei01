from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Perfil({self.user.username})"


class VerificationCode(models.Model):
    CHANNEL_CHOICES = (
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    )
    PURPOSE_CHOICES = (
        ('password_reset', 'Password Reset'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=6)
    channel = models.CharField(max_length=16, choices=CHANNEL_CHOICES)
    purpose = models.CharField(max_length=32, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def mark_used(self):
        self.used = True
        self.save(update_fields=['used'])

    @staticmethod
    def generate_expiry(minutes=10):
        return timezone.now() + timedelta(minutes=minutes)


# Create your models here.
