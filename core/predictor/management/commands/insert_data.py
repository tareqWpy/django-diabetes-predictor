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
        parser.add_argument(
            "-d",
            "--doctor",
            type=bool,
            default=False,
            help="Create doctor",
        )
        parser.add_argument(
            "-p",
            "--patient",
            type=bool,
            default=False,
            help="Create patient",
        )

    def handle(self, *args, **options):
        superuser = options["superuser"]
        doctor = options["doctor"]
        patient = options["patient"]

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

        if doctor:
            try:
                doctor = User.objects.create_user(
                    email="doctor1@admin.com",
                    password="9889taat",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Doctor created successfully! ID: {doctor.id}")
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("Doctor creation failed: Email already exists.")
                )

        if patient:
            try:
                patient = User.objects.create_user(
                    email="patient1@admin.com",
                    password="9889taat",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Patient created successfully! ID: {patient.id}"
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("Patient creation failed: Email already exists.")
                )
