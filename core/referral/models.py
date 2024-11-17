from django.db import models


class ReferralCode(models.Model):
    creator = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)  # doctor
    token = models.CharField(max_length=32, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.creator}: {self.token}"


class ReferralRelation(models.Model):
    refer_from = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="refer_from"
    )  # doctor
    refer_to = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="refer_to",
    )  # patient
    refer_token = models.ForeignKey(
        "referral.ReferralCode",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="refer_token",
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.refer_from} to {self.refer_to} with token {self.refer_token}"
