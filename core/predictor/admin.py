from django.contrib import admin

from .models import Predictor


class PredictorAdmin(admin.ModelAdmin):
    """
    A class for presenting the data in Admin panel.
    """

    model = Predictor
    list_display = (
        "patient",
        "result",
        "created_date",
    )


"""
Registeration for Admin panel to present data of Taks.
"""
admin.site.register(Predictor, PredictorAdmin)
