from django.urls import include, path

app_name = "predictor"
"""
Important urls related to the todo app.
"""
urlpatterns = [
    path("api/v1/", include("predictor.api.v1.urls")),
]
