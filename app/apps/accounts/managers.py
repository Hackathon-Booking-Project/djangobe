from django.contrib.auth.base_user import BaseUserManager
from django.forms import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        """
        Creates and saves a normal user with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save()
        return user
