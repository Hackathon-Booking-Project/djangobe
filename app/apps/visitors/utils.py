from datetime import timedelta, datetime
from django.conf import settings
from django.db.models import Q
from .models import Visitor


BOOKING_RULES = settings.BOOKING_RULES


def get_datetime_from_date_and_time_objects(date, time):
    return datetime(year=date.year, month=date.month, day=date.day,
                    hour=time.hour, minute=time.minute)


def datetime_is_not_expired(timestamp, closing_time):
    return (
        timestamp + timedelta(minutes=BOOKING_RULES["expected_residence"]) <= closing_time
    )


def get_early_exit_timepair_from_timestamp(timestamp):
    early_datetime = timestamp - timedelta(minutes=BOOKING_RULES["expected_residence"])
    exit_datetime = timestamp + timedelta(minutes=BOOKING_RULES["expected_residence"])
    return early_datetime, exit_datetime


def timestamp_is_bookable(timestamp):
    early_datetime, exit_datetime = get_early_exit_timepair_from_timestamp(timestamp)
    visitors = Visitor.objects.filter(
        Q(planed_entry__gt=early_datetime) & Q(planed_entry__lt=exit_datetime)
    )
    return visitors.count() < BOOKING_RULES["max_visitor_capacity"]
