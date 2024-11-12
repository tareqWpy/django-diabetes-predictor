from django.contrib import admin

from .models import DoctorPredictor, Patient, PatientPredictor


class ClientPredictorAdmin(admin.ModelAdmin):
    """
    A class for presenting the data in Admin panel.
    """

    list_display = (
        "id",
        "patient",
        "result",
        "created_date",
    )
    list_filter = ("created_date", "female_age")
    search_fields = ("patient__name",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


class DoctorPredictorAdmin(admin.ModelAdmin):
    """
    A class for presenting the data in Admin panel.
    """

    list_display = (
        "id",
        "doctor",
        "patient",
        "result",
        "created_date",
    )
    list_filter = ("created_date", "female_age")
    search_fields = ("patient__name",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


"""
Registeration for Admin panel to present data of Taks.
"""
admin.site.register(Patient)
admin.site.register(PatientPredictor, ClientPredictorAdmin)
admin.site.register(DoctorPredictor, DoctorPredictorAdmin)
