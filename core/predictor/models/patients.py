from django.db import models


class Patient(models.Model):
    """
    This Django model represents a patient created by a doctor.
    """

    manager = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
