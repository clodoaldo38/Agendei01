from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ServiceCategory, Service, Appointment, BusinessHours


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    def formatted_price(self, obj):
        try:
            return f"R$ {obj.price:.2f}".replace('.', ',')
        except Exception:
            return f"R$ {obj.price}"

    formatted_price.short_description = "Preço"

    list_display = ("name", "provider", "category", "duration_minutes", "formatted_price", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "provider__username")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("service", "customer", "provider", "scheduled_for", "status")
    list_filter = ("status", "provider")
    search_fields = ("customer__username", "provider__username", "service__name")
    date_hierarchy = "scheduled_for"


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ("provider", "day_of_week", "is_closed", "open_time", "close_time")
    list_filter = ("provider", "day_of_week", "is_closed")
    search_fields = ("provider__username",)

    @admin.action(description="Fechar dia selecionado")
    def fechar_dia(self, request, queryset):
        updated = queryset.update(is_closed=True, open_time=None, close_time=None)
        self.message_user(request, f"{updated} dia(s) fechado(s).")

    @admin.action(description="Reabrir dia selecionado")
    def reabrir_dia(self, request, queryset):
        updated = queryset.update(is_closed=False)
        self.message_user(request, f"{updated} dia(s) reaberto(s).")

    actions = ["fechar_dia", "reabrir_dia"]


class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    extra = 0
    fields = ("day_of_week", "is_closed", "open_time", "close_time")
    show_change_link = True


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    inlines = [BusinessHoursInline]


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)

# Register your models here.
