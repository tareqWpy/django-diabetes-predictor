from django.urls import include, path

app_name = "predictor"
"""
Urls related to the predictor app.
"""
urlpatterns = [
    path("api/v1/", include("predictor.api.v1.urls")),
]
