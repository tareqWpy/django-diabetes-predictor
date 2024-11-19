from django.db import models


class ReferralRelationship(models.Model):
    refer_from = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="referrals_made"
    )  # doctor
    refer_to = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="referrals_received",
    )  # patient
    refer_token = models.ForeignKey(
        "referral.ReferralToken",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="referral_relationships",
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.refer_from} to {self.refer_to} with token {self.refer_token}"
