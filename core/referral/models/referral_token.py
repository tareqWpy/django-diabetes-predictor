from django.db import models


class ReferralToken(models.Model):
    creator = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)  # doctor
    token = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.creator}: {self.token}"
