from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Visitor
from .utils import timestamp_is_bookable
from .exceptions import InvalidTimeException, BookingAlreadyExpiredException


class SimpleDateSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ["first_name", "last_name", "email", "street", "street_no",
                  "city", "postcode", "additional", "planed_entry", "department",
                  "key", ]
        extra_kwargs = {
            "key": {"read_only": True}
        }

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=True)
        if not is_valid:
            return False
        entry = self.validated_data["planed_entry"]
        if not timestamp_is_bookable(timestamp=entry) and not raise_exception:
            return False
        elif not timestamp_is_bookable(timestamp=entry) and raise_exception:
            raise ValidationError(
                detail={"planed_entry": f"No booking for {entry} available"}
            )
        else:
            return True


class VisitorAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ["key", "department", "entry", "outgoing", ]
        extra_kwargs = {
            "key": {"read_only": True},
            "department": {"read_only": True},
            "entry": {"read_only": True},
            "outgoing": {"read_only": True}
        }

    def update(self, instance, validated_data):
        if not instance.was_present:
            instance.entry = now()
        else:
            instance.outgoing = now()
        try:
            instance.save()
        except InvalidTimeException:
            raise ValidationError(
                detail={
                    "error": "too_early",
                    "planed_entry": instance.planed_entry
                }
            )
        except BookingAlreadyExpiredException:
            raise ValidationError(
                detail={
                    "error": "booking_expired",
                    "planed_entry": instance.planed_entry
                }
            )
        return instance
