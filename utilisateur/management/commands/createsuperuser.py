from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core.management import CommandError
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = "Create a superuser with custom fields"

    def handle(self, *args, **options):
        # Custom input prompts (skip the default prompts)
        username = input("Username: ")
        email = input("Email address: ")
        password = self._get_password()

        # Prompt for the additional custom field 'date_naissance'
        date_naissance = input("Date de naissance (YYYY-MM-DD): ")

        # Ensure date is in the correct format
        try:
            user = self.UserModel.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                date_naissance=date_naissance,  # Pass the custom field
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
