import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from datetime import timedelta
from random import randint


class Visitor(models.Model):
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=144
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=144
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    street = models.CharField(
        verbose_name=_("Street"),
        max_length=144
    )
    street_no = models.CharField(
        verbose_name=_("Street Number"),
        max_length=10
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=144
    )
    postcode = models.CharField(
        verbose_name=_("Postcode"),
        max_length=9
    )
    additional = models.CharField(
        verbose_name=_("Additional"),
        max_length=144,
        blank=True
    )
    creation_timestamp = models.DateTimeField(
        verbose_name=_("Creation Timestamp"),
        auto_now_add=True
    )
    planed_entry = models.DateTimeField(
        verbose_name=_("Planned Entry")
    )
    entry = models.DateTimeField(
        verbose_name=_("Entry"),
        blank=True,
        null=True
    )
    outgoing = models.DateTimeField(
        verbose_name=_("Exit"),
        blank=True,
        null=True
    )
    was_present = models.BooleanField(
        verbose_name=_("Was Present"),
        default=False,
        editable=False
    )
    key = models.PositiveIntegerField(
        verbose_name=_("Key"),
        db_index=True
    )
    department = models.ForeignKey(
        to="accounts.Department",
        on_delete=models.PROTECT,
        related_name="visitors",
        verbose_name=_("Department"),
        db_index=True
    )

    class Meta:
        verbose_name = _("Visitor")
        verbose_name_plural = _("Visitors")
        ordering = ('-creation_timestamp', )
        unique_together = ('key', 'department', )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        else:
            if not self.was_present:
                if self.outgoing:
                    raise ValidationError("Can't go out without were present.")
                if self.is_expired:
                    raise ValidationError("Visitor is already expired.")
                if self.entry:
                    self.was_present = True
        return super().save(*args, **kwargs)

    def generate_key(self):
        key = randint(100000, 999999)
        while Visitor.objects.filter(key=key, department=self.department).exists():
            self.generate_key()
        return key

    @property
    def is_expired(self):
        expiration_time = int(os.getenv("EXPIRATION_TIME_IN_MINUTES", 15))
        expiration_date = now() + timedelta(minutes=expiration_time)
        return expiration_date < self.planed_entry
