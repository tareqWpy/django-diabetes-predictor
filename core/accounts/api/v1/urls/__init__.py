from django.urls import include, path

app_name = "api-v1"

urlpatterns = [
    path("profile/", include("accounts.api.v1.urls.profiles")),
    path("users/", include("accounts.api.v1.urls.users")),
]
