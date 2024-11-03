from django.urls import include, path

from .. import views

urlpatterns = [
    path("", views.ProfileAPIView.as_view(), name="profile"),
]
