from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core.management import CommandError
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = "Create a superuser with custom fields"

    def handle(self, *args, **options):
        # Custom input prompts (skip the default prompts)
        username = input("Username: ")
        email = input("Email address: ")
        password = self._get_password()

        # Prompt for the additional custom field 'date_naissance'
        date_naissance = self._get_date_naissance()

        try:
            user = self.UserModel.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                date_naissance=date_naissance,
            )
        except ValueError as e:
            raise CommandError(str(e))

        self.stdout.write(
            self.style.SUCCESS(f"Superuser {user.username} created successfully!")
        )

    def _get_password(self):
        """
        Prompt for password and handle validation.
        """
        while True:
            password = input("Password: ")
            password2 = input("Password (again): ")
            if password != password2:
                self.stderr.write(self.style.ERROR("Passwords don't match"))
            else:
                return password

    def _get_date_naissance(self):
        while True:
            date_input = input("Date de naissance (YYYY-MM-DD): ")
            try:
                date_naissance = parse_date(date_input)
            except ValueError:
                date_naissance = None

            if date_naissance is None:
                self.stderr.write(
                    self.style.ERROR("Date invalide. Utilisez le format YYYY-MM-DD.")
                )
                continue
            return date_naissance
