from django.contrib import admin

from .models import DoctorPredictor, Patient, PatientPredictor


class ClientPredictorAdmin(admin.ModelAdmin):
    """
    A class for Client to present data in Admin panel.
    """

    list_display = (
        "id",
        "get_full_name",
        "client",
        "result",
        "created_date",
    )
    list_filter = ("created_date", "female_age")
    search_fields = ("client__first_name", "client__last_name")
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


class DoctorPredictorAdmin(admin.ModelAdmin):
    """
    A class for Doctor to present data in Admin panel.
    """

    list_display = (
        "id",
        "get_full_name",
        "doctor",
        "patient",
        "result",
        "created_date",
    )
    list_filter = ("created_date", "female_age")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "doctor__first_name",
        "doctor__last_name",
    )
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


class PatientAdmin(admin.ModelAdmin):
    """
    A class for Patient to present data in Admin panel.
    """

    list_display = (
        "id",
        "manager",
        "get_full_name",
        "created_date",
        "updated_date",
    )
    list_filter = ("created_date",)
    search_fields = ("manager__first_name", "manager__last_name")
    ordering = ("-created_date",)
    readonly_fields = ("created_date",)


"""
Registeration classes for Admin panel.
"""
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientPredictor, ClientPredictorAdmin)
admin.site.register(DoctorPredictor, DoctorPredictorAdmin)
