from django.contrib import admin

from .models import Predictor


class PredictorAdmin(admin.ModelAdmin):
    """
    A class for Predictor model to present data in Admin panel.
    """

    list_display = (
        "id",
        "result",
        "created_date",
    )
    ordering = ("-created_date",)


"""
Registeration classes for Admin panel.
"""

admin.site.register(Predictor, PredictorAdmin)
