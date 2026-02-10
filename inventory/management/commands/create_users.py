from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create default users: hazmat and frv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--set-passwords',
            action='store_true',
            help='Prompt to set passwords for the users',
        )

    def handle(self, *args, **options):
        users_to_create = [
            {
                'username': 'hazmat',
                'email': 'hazmat@example.com',
                'first_name': 'Hazmat',
                'last_name': 'User'
            },
            {
                'username': 'frv',
                'email': 'frv@example.com',
                'first_name': 'FRV',
                'last_name': 'User'
            }
        ]

        for user_data in users_to_create:
            username = user_data['username']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists')
                )
                continue
            
            # Determine password
            if options['set_passwords']:
                # Prompt for password
                password = self.get_password_from_prompt(username)
            else:
                # Use a default password
                password = 'defaultpass123'
                self.stdout.write(
                    self.style.WARNING(
                        f'Using default password for {username}. '
                        f'Please change it after login.'
                    )
                )
            
            # Create the user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password,
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created user "{username}" with ID {user.id}'
                )
            )

    def get_password_from_prompt(self, username):
        """Prompt for password securely"""
        import getpass
        
        while True:
            password = getpass.getpass(f'Enter password for {username}: ')
            confirm_password = getpass.getpass(f'Confirm password for {username}: ')
            
            if password == confirm_password:
                if len(password) < 8:
                    self.stdout.write(
                        self.style.ERROR(
                            'Password is too short. It must be at least 8 characters.'
                        )
                    )
                    continue
                return password
            else:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match. Please try again.')
                )