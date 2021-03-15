from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.timezone import now
from django.db.models import Q
from datetime import timedelta, datetime
from django.conf import settings
from .models import Visitor


BOOKING_RULES = settings.BOOKING_RULES


class TerminAPI(GenericAPIView):
    def retrieve_day_planning(self, request, *args, **kwargs):
        pass

    def retrieve_date_planning(self, request, *args, **kwargs):
        current_timestamp = now()
        dates = []
        for day in range(BOOKING_RULES["max_days_in_future"]):
            current_time = datetime(
                year=current_timestamp.year,
                month=current_timestamp.month,
                day=current_timestamp.day,
                hour=BOOKING_RULES["opening"].hour,
                minute=BOOKING_RULES["opening"].minute
            )
            closing = datetime(
                year=current_timestamp.year,
                month=current_timestamp.month,
                day=current_timestamp.day,
                hour=BOOKING_RULES["closing"].hour,
                minute=BOOKING_RULES["closing"].minute
            )
            is_bookable = False
            while current_time + timedelta(minutes=BOOKING_RULES["expected_residence"]) < closing:
                early_datetime = current_time - timedelta(minutes=BOOKING_RULES["inacuracy"])
                exit_datetime = (
                    current_time + timedelta(minutes=BOOKING_RULES["expected_residence"])
                )
                visitors = Visitor.objects.filter(
                    Q(planed_entry__gte=early_datetime) &
                    Q(planed_entry__lte=exit_datetime)
                )
                is_bookable = visitors.count() < BOOKING_RULES["max_visitor_capacity"]
                if is_bookable:
                    break
                current_time = current_time + timedelta(minutes=BOOKING_RULES["frequence"])
            dates.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "is_bookable": is_bookable
            })
            current_timestamp = current_timestamp + timedelta(days=1)
        return Response(data=dates, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        date = request.GET.get("date", None)
        if date is not None:
            return self.retrieve_day_planning(request, *args, **kwargs)
        return self.retrieve_date_planning(request, *args, **kwargs)
