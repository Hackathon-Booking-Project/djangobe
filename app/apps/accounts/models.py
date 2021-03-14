from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


class Department(models.Model):
    department_identifier = models.CharField(
        verbose_name=_("Department Identifier"),
        max_length=144,
        unique=True,
        db_index=True
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
        max_length=144
    )

    def __str__(self):
        return self.location


class User(AbstractBaseUser):
    from .managers import UserManager

    email = models.EmailField(
        verbose_name=_("Email"),
        blank=True,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=255
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=255
    )
    is_admin = models.BooleanField(
        verbose_name=_("Is Admin"),
        default=False
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        default=True
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name=_("Department"),
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, Auth):
        # "Does the user have permissions to view the app Auth?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
