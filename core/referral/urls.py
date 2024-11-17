from django.urls import include, path

app_name = "referral"
"""
Urls related to the referral app.
"""
urlpatterns = [
    path("api/v1/", include("referral.api.v1.urls")),
]
