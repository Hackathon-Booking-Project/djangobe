from django.core.exceptions import ValidationError


class BookingAlreadyExpiredException(ValidationError):
    pass


class InvalidTimeException(ValidationError):
    pass
