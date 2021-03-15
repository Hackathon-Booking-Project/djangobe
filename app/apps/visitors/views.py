from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.timezone import now
from datetime import timedelta, datetime
from .models import Visitor
from .serializers import SimpleDateSerializer, BookingSerializer
from .utils import (
    get_datetime_from_date_and_time_objects, datetime_is_not_expired,
    timestamp_is_bookable, BOOKING_RULES
)


class TerminAPI(GenericAPIView):
    def get_day_planning(self, date):
        current_time = get_datetime_from_date_and_time_objects(
            date=datetime.strptime(date, "%Y-%m-%d"),
            time=BOOKING_RULES["opening"]
        )
        closing = get_datetime_from_date_and_time_objects(
            date=datetime.strptime(date, "%Y-%m-%d"),
            time=BOOKING_RULES["closing"]
        )
        times = []
        while datetime_is_not_expired(timestamp=current_time, closing_time=closing):
            is_bookable = timestamp_is_bookable(timestamp=current_time)
            times.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M"),
                "is_bookable": is_bookable
            })
            current_time = current_time + timedelta(minutes=BOOKING_RULES["frequence"])
        return times

    def get_date_planning(self):
        current_timestamp = now()
        dates = []
        for day in range(BOOKING_RULES["max_days_in_future"]):
            current_time = get_datetime_from_date_and_time_objects(
                date=current_timestamp,
                time=BOOKING_RULES["opening"]
            )
            closing = get_datetime_from_date_and_time_objects(
                date=current_timestamp,
                time=BOOKING_RULES["closing"]
            )
            is_bookable = False
            while datetime_is_not_expired(timestamp=current_time, closing_time=closing):
                is_bookable = timestamp_is_bookable(timestamp=current_time)
                if is_bookable:
                    break
                current_time = current_time + timedelta(minutes=BOOKING_RULES["frequence"])
            dates.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "is_bookable": is_bookable
            })
            current_timestamp = current_timestamp + timedelta(days=1)
        return dates

    def retrieve_day_planning(self, request, date, *args, **kwargs):
        serializer = SimpleDateSerializer(data={"date": date})
        serializer.is_valid(raise_exception=True)
        day_planning = self.get_day_planning(date=date)
        return Response(data=day_planning, status=status.HTTP_200_OK)

    def retrieve_date_planning(self, request, *args, **kwargs):
        date_planning = self.get_date_planning()
        return Response(data=date_planning, status=status.HTTP_200_OK)

    def create_booking(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        date = request.GET.get("date", None)
        if date is not None:
            return self.retrieve_day_planning(request, date=date, *args, **kwargs)
        return self.retrieve_date_planning(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create_booking(request, *args, **kwargs)
