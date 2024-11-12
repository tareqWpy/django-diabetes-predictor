from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class DoctorPredictor(models.Model):
    """
    Doctor Predictor Model

    This Django model represents a predictor for assisted reproductive technology outcomes.
    It contains various medical parameters relevant to fertility assessments for individual patients.

    Attributes:
    - patient (ForeignKey): A reference to the associated patient, linked to the Profile model in the accounts app.
    - female_age (IntegerField): The age of the female patient in years.
    - AMH (DecimalField): Anti-Müllerian hormone level, a marker for ovarian reserve.
    - FSH (DecimalField): Follicle-stimulating hormone level, indicative of ovulatory function.
    - no_embryos (IntegerField): The number of embryos retrieved during the procedure.
    - endoendometrial_tickness (DecimalField): Thickness of the endometrium, important for implantation.
    - sperm_count (DecimalField): Total sperm count available for fertilization.
    - sperm_morphology (IntegerField): Quality of sperm morphology as assessed under a microscope.
    - follicle_size (IntegerField): Average size of the ovarian follicles, crucial for ovulation timing.
    - no_of_retrieved_oocytes (IntegerField): Number of oocytes retrieved during the egg retrieval process.
    - qality_of_embryo (IntegerField): Quality assessment of the embryos.
    - quality_of_retrieved_oocytes_MI (IntegerField): Quality assessment of retrieved oocytes at the metaphase I stage.
    - quality_of_retrieved_oocytes_MII (IntegerField): Quality assessment of retrieved oocytes at the metaphase II stage.
    - result (IntegerField): The final result of the prediction model.
    - created_date (DateTimeField): Timestamp for when the predictor record was created, auto-filled upon creation.

    Methods:
    - __str__(): Returns a string representation of the predictor instance, including the patient and results.
    - get_absolute_api_url(): Returns the API endpoint URL for accessing details of the predictor instance.
    """

    doctor = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    patient = models.ForeignKey("Patient", on_delete=models.SET_NULL, null=True)
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

    def __str__(self):
        return f"Predictor for {self.patient} - Result: {self.result}"

    def get_absolute_api_url(self):
        return reverse(
            "predictor:api-v1:doctor-predictor-detail", kwargs={"pk": self.pk}
        )
