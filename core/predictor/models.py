from django.db import models
from django.urls import reverse


class Diabetes(models.Model):

    pregnancies = models.IntegerField()
    glucose = models.IntegerField()
    blood_pressure = models.IntegerField()
    skin_thickness = models.IntegerField()
    insulin = models.IntegerField()
    bmi = models.DecimalField(max_digits=4, decimal_places=1)
    diabetes_pedigree_function = models.DecimalField(max_digits=4, decimal_places=3)
    age = models.IntegerField()
    outcome = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_api_url(self):
        return reverse("predictor:api-v1:predictor-detail", kwargs={"pk": self.pk})
