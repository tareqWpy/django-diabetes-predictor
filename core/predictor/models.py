from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Predictor(models.Model):

    female_age = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(99)]
    )
    AMH = models.DecimalField(max_digits=4, decimal_places=2)
    FSH = models.DecimalField(max_digits=4, decimal_places=2)
    no_embryos = models.IntegerField()
    endoendometerial_tickness = models.DecimalField(max_digits=4, decimal_places=2)
    sperm_count = models.DecimalField(max_digits=4, decimal_places=2)
    sperm_morphology = models.IntegerField()
    follicle_size = models.IntegerField()
    no_of_retreived_oocytes = models.IntegerField()
    qality_of_embryo = models.IntegerField()
    quality_of_retreived_oocytes_MI = models.IntegerField()
    quality_of_retreived_oocytes_MII = models.IntegerField()
    result = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_api_url(self):
        return reverse("predictor:api-v1:predictor-detail", kwargs={"pk": self.pk})
