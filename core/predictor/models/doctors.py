from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class DoctorPredictor(models.Model):
    """
    Represents a predictor for assisted reproductive technology outcomes.

    This model captures various fertility-related medical parameters for individual patients, facilitating assessments
    of their likelihood of successful outcomes in assisted reproductive procedures.

    Attributes:
        doctor (ForeignKey):
            A reference to the associated doctor, linked to the Profile model in the accounts app.
        patient (ForeignKey):
            A reference to the associated patient, linked to the Profile model in the accounts app.
            This can be null if no patient is associated.
        female_age (IntegerField):
            The age of the female patient in years, validated to be between 10 and 99.
        AMH (DecimalField):
            Anti-Müllerian hormone level, indicating ovarian reserve.
        FSH (DecimalField):
            Follicle-stimulating hormone level, relevant for evaluating ovulatory function.
        no_embryos (IntegerField):
            The number of embryos retrieved during the procedure.
        endoendometrial_tickness (DecimalField):
            Thickness of the endometrium, important for implantation success.
        sperm_count (DecimalField):
            Total sperm count available for fertilization, measured in millions.
        sperm_morphology (IntegerField):
            Assessment of sperm morphology as evaluated under a microscope.
        follicle_size (IntegerField):
            Average size of ovarian follicles, important for ovulation timing.
        no_of_retrieved_oocytes (IntegerField):
            Total number of oocytes retrieved during the egg retrieval process.
        quality_of_embryo (IntegerField):
            Quality assessment rating for the retrieved embryos.
        quality_of_retrieved_oocytes_MI (IntegerField):
            Quality assessment rating for acquired oocytes at the metaphase I stage.
        quality_of_retrieved_oocytes_MII (IntegerField):
            Quality assessment rating for acquired oocytes at the metaphase II stage.
        result (IntegerField):
            The final predictive result from the model.
        created_date (DateTimeField):
            Timestamp of when the predictor instance was created, auto-filled upon record creation.

    Methods:
        __str__():
            Returns a string representation of the predictor instance, including associated doctor and patient details.
        get_absolute_api_url():
            Returns the API endpoint URL for accessing details of the predictor instance.
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
        return f"Doctor: {self.doctor} - Patient: {self.patient}"

    def get_absolute_api_url(self):
        return reverse(
            "predictor:api-v1:doctor-predictor-detail", kwargs={"pk": self.pk}
        )

    def get_full_name(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"
