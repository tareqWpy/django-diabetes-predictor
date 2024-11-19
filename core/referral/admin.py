from django.contrib import admin

from .models import ReferralToken


@admin.register(ReferralToken)
class CostumReferralAdmin(admin.ModelAdmin):
    list_display = ("creator", "token")
    searching_fields = ("creator", "token")
