from django.db import models


class Referral(models.Model):
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
    refer_token = models.CharField(max_length=255)
    is_expired = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.refer_from} to {self.refer_to} with token {self.refer_token}"
