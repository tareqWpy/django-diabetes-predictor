from django.db import models
from django.urls import reverse


class Patient(models.Model):
    """
    Represents a patient in the system created by a doctor.

    Attributes:
        manager (ForeignKey): A reference to the Profile of the managing doctor.
        first_name (CharField): The patient's first name, limited to 255 characters.
        last_name (CharField): The patient's last name, limited to 255 characters.
        created_date (DateTimeField): The date and time when the patient record was created, auto-populated on creation.
        updated_date (DateTimeField): The date and time when the patient record was last updated, auto-populated on each update.

    Methods:
        __str__(): Returns the patient's full name in the format "First Last".
    """

    manager = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_api_url(self):
        return reverse("predictor:api-v1:patient-detail", kwargs={"pk": self.pk})
