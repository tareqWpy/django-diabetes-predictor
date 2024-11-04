from django.db import models
from django.urls import reverse


class Predictor(models.Model):
    patient = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    female_age = models.PositiveIntegerField()  # Assuming age is a positive integer
    AMH = models.FloatField()  # Anti-Müllerian hormone level
    FSH = models.FloatField()  # Follicle-stimulating hormone level
    no_embryos = models.PositiveIntegerField()  # Number of embryos
    endoendometrial_thickness = models.FloatField()  # Endometrial thickness in mm
    sperm_count = models.PositiveIntegerField()  # Sperm count
    sperm_morphology = models.FloatField()  # Sperm morphology percentage
    follicle_size = models.FloatField()  # Size of follicles in mm
    retrieved_oocytes = models.PositiveIntegerField()  # Number of retrieved oocytes
    quality_of_embryo = models.CharField(
        max_length=255,
    )  # Quality of embryos as a string
    retrieved_oocytes_MI = models.PositiveIntegerField()  # Mature oocytes (MI stage)
    retrieved_oocytes_MII = models.PositiveIntegerField()  # Mature oocytes (MII stage)
    result = models.CharField(
        max_length=255,
    )  # Outcome/result as a string

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predictor for {self.patient} - Result: {self.result}"

    def get_absolute_api_url(self):
        return reverse("predictor:api-v1:predictor-detail", kwargs={"pk": self.pk})
