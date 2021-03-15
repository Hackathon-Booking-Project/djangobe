from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Visitor
from .utils import timestamp_is_bookable


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
