from decouple import config
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UtilisateurManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Send the email after the user is created
        subject = _("Welcome to the System")
        message = f"Hello {user.username},\n\nYour account has been successfully created.\n\nUsername: {user.username}\nPassword: {password}\n\nThank you!"
        from_email = config("DEFAULT_FROM_EMAIL")
        send_mail(subject, message, from_email, [user.email])

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure date_naissance is provided when creating a superuser
        if not extra_fields.get("date_naissance"):
            raise ValueError(_("The date_naissance field must be set for superusers"))

        extra_fields.setdefault("role", "adminsystem")
        return self.create_user(username, email, password, **extra_fields)
