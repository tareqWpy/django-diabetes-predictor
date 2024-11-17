import random

from accounts.models import Profile, User, UserType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker

from ...models import Predictor


class Command(BaseCommand):
    help = "Inserting dummy data into the database"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--superuser",
            type=bool,
            default=False,
            help="Create superuser",
        )

    def handle(self, *args, **options):
        superuser = options["superuser"]

        if superuser:
            try:
                superuser = User.objects.create_superuser(
                    email="admin@admin.com",
                    password="9889taat",
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Superuser created successfully! ID: {superuser.id}"
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        "Superuser creation failed: Email already exists."
                    )
                )
