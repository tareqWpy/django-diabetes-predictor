from django.contrib import admin

from .models import ReferralCode


@admin.register(ReferralCode)
class CostumReferralAdmin(admin.ModelAdmin):
    list_display = ("creator", "token")
    searching_fields = ("creator", "token")
