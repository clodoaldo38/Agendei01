from rest_framework import generics, permissions

from .models import Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True).select_related("provider", "category")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]