from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

# Initialize a DefaultRouter instance to automatically generate routes for the registered viewsets.
router = DefaultRouter()

router.register(
    "referrals",
    viewset=views.ReferralTokenViewset,
    basename="referrals",
)

router.register(
    "get-relations",
    viewset=views.ReferralRelationshipViewset,
    basename="get-relations",
)

router.register(
    "anon_get_referrals",
    viewset=views.AnonReferralTokenViewset,
    basename="anon_get_referrals",
)
# The urlpatterns variable will hold the URL patterns generated by the router.
urlpatterns = router.urls
