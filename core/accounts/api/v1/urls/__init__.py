from django.urls import include, path

urlpatterns = [
    path("profile/", include("accounts.api.v1.urls.profiles")),
]
