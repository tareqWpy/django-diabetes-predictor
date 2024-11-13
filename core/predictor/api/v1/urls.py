from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

# Initialize a DefaultRouter instance to automatically generate routes for the registered viewsets.
router = DefaultRouter()

router.register(
    "doctor",
    viewset=views.PredictionByDoctorViewSet,
    basename="doctor-predictor",
)
router.register(
    "client",
    viewset=views.PredictionByClientViewSet,
    basename="client-predictor",
)
router.register("patient", viewset=views.PatientModelViewSet, basename="patient")

# The urlpatterns variable will hold the URL patterns generated by the router.
urlpatterns = router.urls
