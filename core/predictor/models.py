from django.db import models
from django.urls import reverse


class Predictor(models.Model):
    """
    Predictor Model

    This Django model represents a predictor for assisted reproductive technology outcomes.
    It contains various medical parameters relevant to fertility assessments and prediction of success probabilities for individual patients.

    Attributes:
    - patient (ForeignKey): A reference to the associated patient, linked to the Profile model in the accounts app.
    - female_age (FloatField): The age of the female patient in years.
    - AMH (FloatField): Anti-Müllerian hormone level, a marker for ovarian reserve.
    - FSH (FloatField): Follicle-stimulating hormone level, indicative of ovulatory function.
    - no_embryos (FloatField): The number of embryos retrieved during the procedure.
    - endoendometrial_tickness (FloatField): Thickness of the endometrium, important for implantation.
    - sperm_count (FloatField): Total sperm count available for fertilization.
    - sperm_morphology (FloatField): Quality of sperm morphology as assessed under a microscope.
    - follicle_size (FloatField): Average size of the ovarian follicles, crucial for ovulation timing.
    - no_of_retrieved_oocytes (FloatField): Number of oocytes retrieved during the egg retrieval process.
    - qality_of_embryo (FloatField): Quality assessment of the embryos.
    - quality_of_retrieved_oocytes_MI (FloatField): Quality assessment of retrieved oocytes at the metaphase I stage.
    - quality_of_retrieved_oocytes_MII (FloatField): Quality assessment of retrieved oocytes at the metaphase II stage.
    - result (FloatField): The final result of the prediction model.
    - success_probability (FloatField): The predicted probability of success for the treatment, defaults to 0 if not set.
    - created_date (DateTimeField): Timestamp for when the predictor record was created, auto-filled upon creation.

    Methods:
    - __str__(): Returns a string representation of the predictor instance, including the patient and results.
    - get_absolute_api_url(): Returns the API endpoint URL for accessing details of the predictor instance.

    Usage:
    This model can be utilized within a fertility clinic's application to record and analyze predictors of treatment success, enabling personalized patient care and informed decision-making.
    """

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
