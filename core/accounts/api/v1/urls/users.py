from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .. import views

router = DefaultRouter()
router.register(
    "users",
    viewset=views.CustomUserViewSet,
    basename="users",
)
urlpatterns = router.urls


urlpatterns += [
    path(
        "delete_account/", views.AccountDeleteAPIView.as_view(), name="delete-account"
    ),
]
