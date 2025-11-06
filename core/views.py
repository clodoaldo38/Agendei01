from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Service


def home(request):
    # Fluxo: não autenticado vai para login; autenticado para boas-vindas
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('welcome')


@login_required
def services(request):
    services_qs = Service.objects.filter(is_active=True).select_related('provider', 'category')
    return render(request, 'services.html', { 'services': services_qs })


@login_required
def welcome(request):
    return render(request, 'welcome.html')

# Create your views here.
