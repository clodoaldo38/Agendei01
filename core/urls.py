from django.urls import path
from .views import home, services
from .api import ServiceListAPIView, AppointmentCreateAPIView

urlpatterns = [
    path('', home, name='home'),
    path('servicos/', services, name='services'),
    # API endpoints
    path('api/services/', ServiceListAPIView.as_view(), name='api_services_list'),
    path('api/appointments/', AppointmentCreateAPIView.as_view(), name='api_appointments_create'),
]