from django.db import models
from django.conf import settings


class ServiceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('provider', 'name'),)
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.provider})"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('completed', 'Concluído'),
        ('canceled', 'Cancelado'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provided_appointments')
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['provider', 'scheduled_for']),
            models.Index(fields=['customer', 'scheduled_for']),
        ]
        ordering = ['-scheduled_for']

    def __str__(self):
        return f"Agendamento de {self.customer} para {self.service} em {self.scheduled_for}"


class BusinessHours(models.Model):
    DAYS = (
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_hours')
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS)
    is_closed = models.BooleanField(default=False)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('provider', 'day_of_week'),)
        ordering = ['provider', 'day_of_week']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {'Fechado' if self.is_closed else f'{self.open_time} às {self.close_time}'} ({self.provider})"


# Create your models here.
