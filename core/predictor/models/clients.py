from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class PatientPredictor(models.Model):
    """
    Patient Predictor Model

    This Django model represents predictors for outcomes in assisted reproductive technology.
    It captures essential medical parameters for evaluating fertility potential in individual patients.

    Attributes:
        client (ForeignKey): A reference to the associated patient, linked to the Profile model in the accounts app.
        female_age (IntegerField): Age of the female patient in years, validated between 10 and 99.
        AMH (DecimalField): Anti-Müllerian hormone level, a key marker for ovarian reserve.
        FSH (DecimalField): Follicle-stimulating hormone level, indicating ovulatory function.
        no_embryos (IntegerField): Number of embryos retrieved during the procedure.
        endometrial_thickness (DecimalField): Thickness of the endometrium, significant for implantation success.
        sperm_count (DecimalField): Total sperm count available for fertilization.
        sperm_morphology (IntegerField): Quality of sperm morphology as evaluated microscopically.
        follicle_size (IntegerField): Average size of the ovarian follicles, important for timing ovulation.
        no_of_retrieved_oocytes (IntegerField): Number of oocytes retrieved during the egg retrieval process.
        quality_of_embryo (IntegerField): Quality assessment score of the embryos.
        quality_of_retrieved_oocytes_MI (IntegerField): Quality assessment of retrieved oocytes at metaphase I.
        quality_of_retrieved_oocytes_MII (IntegerField): Quality assessment of retrieved oocytes at metaphase II.
        result (IntegerField): Final output of the prediction model.
        created_date (DateTimeField): Timestamp for record creation, auto-filled upon creation.

    Methods:
        __str__(): Returns a string representation of the predictor instance, including patient details and results.
        get_absolute_api_url(): Returns the URL for accessing the detail view of the predictor instance via API.
    """

    client = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
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
        return f"Predictor for {self.client} - Result: {self.result}"

    def get_absolute_api_url(self):
        return reverse(
            "predictor:api-v1:client-predictor-detail", kwargs={"pk": self.pk}
        )

    def get_full_name(self):
        return f"{self.client.first_name} {self.client.last_name}"
