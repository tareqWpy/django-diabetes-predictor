from django.db import models
from django.urls import reverse


class Predictor(models.Model):
    patient = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    female_age = models.FloatField()
    AMH = models.FloatField()
    FSH = models.FloatField()
    no_embryos = models.FloatField()
    endoendometerial_tickness = models.FloatField()
    sperm_count = models.FloatField()
    sperm_morphology = models.FloatField()
    follicle_size = models.FloatField()
    no_of_retreived_oocytes = models.FloatField()
    qality_of_embryo = models.FloatField()
    quality_of_retreived_oocytes_MI = models.FloatField()
    quality_of_retreived_oocytes_MII = models.FloatField()
    result = models.FloatField()
    success_probability = models.FloatField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predictor for {self.patient} - Result: {self.result} - success_probability: {self.success_probability}"

    def get_absolute_api_url(self):
        return reverse("predictor:api-v1:predictor-detail", kwargs={"pk": self.pk})
