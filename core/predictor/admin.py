from django.contrib import admin

from .models import Predictor


class PredictorAdmin(admin.ModelAdmin):
    """
    A class for Predictor model to present data in Admin panel.
    """

    list_display = (
        "id",
        "get_full_name",
        "patient",
        "result",
        "created_date",
    )
    list_filter = ("created_date", "female_age")
    search_fields = ("patient__first_name", "patient__last_name")
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


"""
Registeration classes for Admin panel.
"""

admin.site.register(Predictor, PredictorAdmin)
