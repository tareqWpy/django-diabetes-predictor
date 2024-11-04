from accounts.models import Profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from ...models import Predictor
from .paginations import DefaultPagination
from .serializers import PredictorSerializers


class PredictorModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [IsAuthenticated]
    serializer_class = PredictorSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {"result": ["exact"], "created_date": ["gte", "lte"]}
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Predictor.objects.none()

        return Predictor.objects.filter(patient=profile)
