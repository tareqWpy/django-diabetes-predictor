from django.urls import include, path

# The application name
app_name = "accounts"
"""
Urls related to the accounts app.
"""

urlpatterns = [
    # ? Commented out URL patterns for API v1 (uncomment to use)
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.jwt")),
    path("api/v1/", include("accounts.api.v1.urls")),
]
