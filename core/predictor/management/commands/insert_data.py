import random

from accounts.models import Profile, User, UserType
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker

from ...models import DoctorPredictor, Patient, PatientPredictor


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
            "-c",
            "--client",
            type=bool,
            default=False,
            help="Client users to create",
        )
        parser.add_argument(
            "-d",
            "--doctor",
            type=bool,
            default=False,
            help="Doctor users to create",
        )
        parser.add_argument(
            "-p",
            "--patient",
            type=int,
            default=0,
            help="Number of patients to create",
        )

    def handle(self, *args, **options):
        superuser = options["superuser"]
        client = options["client"]
        doctor = options["doctor"]

        if superuser:
            try:
                superuser = User.objects.create_superuser(
                    email="admin@admin2.com",
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

        if client:
            try:
                client_user = User.objects.create_user(
                    email="client@admin2.com",
                    password="9889taat",
                    is_active=True,
                    type=UserType.client.value,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Client created successfully! ID: {client_user.id}"
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("Client creation failed: Email already exists.")
                )

        if doctor:
            try:
                doctor_user = User.objects.create_user(
                    email="doctor@admin2.com",
                    password="9889taat",
                    is_active=True,
                    type=UserType.doctor.value,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Doctor created successfully! ID: {doctor_user.id}"
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("Doctor creation failed: Email already exists.")
                )
