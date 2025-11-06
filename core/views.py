from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Service


def home(request):
    return render(request, 'home.html')


@login_required
def services(request):
    services_qs = Service.objects.filter(is_active=True).select_related('provider', 'category')
    return render(request, 'services.html', { 'services': services_qs })

# Create your views here.
