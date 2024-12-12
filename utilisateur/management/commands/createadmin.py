# utilisateur/management/commands/createadmin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username for the admin user')
        parser.add_argument('--email', type=str, required=True, help='Email address for the admin user')
        parser.add_argument('--password', type=str, required=True, help='Password for the admin user')
        parser.add_argument('--nom', type=str, required=True, help='Last name for the admin user')
        parser.add_argument('--prenom', type=str, required=True, help='First name for the admin user')
        parser.add_argument('--date_naissance', type=str, required=True, help='Date of birth for the admin user (YYYY-MM-DD)')
        parser.add_argument('--telephone', type=str, required=True, help='Telephone number for the admin user')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']
        nom = options['nom']
        prenom = options['prenom']
        date_naissance = options['date_naissance']
        telephone = options['telephone']

        if User.objects.filter(username=username).exists():
            raise CommandError('Username "%s" is already taken' % username)

        if User.objects.filter(email=email).exists():
            raise CommandError('Email "%s" is already taken' % email)

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance,
            telephone=telephone,
            role='Admin'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created admin user "%s"' % username))