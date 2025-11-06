from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Service, Appointment, BusinessHours


class ServiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="provider.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "duration_minutes",
            "price",
            "is_active",
            "provider",
            "provider_name",
            "category",
            "category_name",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.filter(is_active=True))

    class Meta:
        model = Appointment
        fields = [
            "id",
            "service",
            "provider",
            "customer",
            "scheduled_for",
            "status",
            "notes",
        ]
        read_only_fields = ["provider", "customer", "status"]

    def validate(self, attrs):
        request = self.context.get("request")
        service: Service = attrs.get("service")
        scheduled_for = attrs.get("scheduled_for")

        if not service:
            raise serializers.ValidationError("Serviço é obrigatório.")
        if not scheduled_for:
            raise serializers.ValidationError("Data/hora do agendamento é obrigatória.")

        # Compute end time based on service duration
        end_time = scheduled_for + timedelta(minutes=service.duration_minutes)

        # Business hours validation
        weekday = scheduled_for.weekday()
        try:
            bh = BusinessHours.objects.get(provider=service.provider, day_of_week=weekday)
        except BusinessHours.DoesNotExist:
            raise serializers.ValidationError("Prestador não possui horário configurado para este dia.")

        if bh.is_closed:
            raise serializers.ValidationError("Prestador está fechado neste dia.")

        # Ensure within open/close window (if defined)
        if bh.open_time and bh.close_time:
            start_t = scheduled_for.time()
            end_t = end_time.time()
            # start should be on/after open, end should be on/before close
            if start_t < bh.open_time or end_t > bh.close_time:
                raise serializers.ValidationError("Horário fora da janela de funcionamento.")

        # Conflict validation: overlapping appointments for provider
        existing = Appointment.objects.filter(
            provider=service.provider,
            status__in=["pending", "confirmed", "completed"],
        )

        for ap in existing:
            ap_end = ap.scheduled_for + timedelta(minutes=ap.service.duration_minutes)
            overlaps = scheduled_for < ap_end and end_time > ap.scheduled_for
            if overlaps:
                raise serializers.ValidationError("Conflito com outro agendamento do prestador.")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        service: Service = validated_data["service"]
        validated_data["provider"] = service.provider
        if request and request.user and request.user.is_authenticated:
            validated_data["customer"] = request.user
        else:
            raise serializers.ValidationError("Autenticação necessária para agendar.")

        # Default status
        validated_data.setdefault("status", "pending")
        return super().create(validated_data)