# Correct the path to point to the 'services' directory
import os
from pathlib import Path

import joblib
import sklearn
from accounts.models import Profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...models import Predictor
from .paginations import DefaultPagination
from .serializers import PredictorSerializers

SERVICES_DIR = Path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "services")
)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        scaled_data = self.preprocess_data(validated_data)
        result = self.get_prediction(scaled_data)

        # Save the predictor with result
        predictor = serializer.save(result=result)

        return Response(
            {
                "details": {
                    "result": predictor.result,
                }
            },
            status=status.HTTP_201_CREATED,
        )

    def preprocess_data(self, data):
        scaler_file_path = SERVICES_DIR.joinpath("scaler.pkl")
        scaler = joblib.load(scaler_file_path)
        features = [
            data["female_age"],
            data["AMH"],
            data["FSH"],
            data["no_embryos"],
            data["endoendometerial_tickness"],
            data["sperm_count"],
            data["sperm_morphology"],
            data["follicle_size"],
            data["no_of_retreived_oocytes"],
            data["qality_of_embryo"],
            data["quality_of_retreived_oocytes_MI"],
            data["quality_of_retreived_oocytes_MII"],
        ]

        print([features])
        print(scaler.transform([features]))
        return scaler.transform([features])

    def get_prediction(self, data):
        model_file_path = SERVICES_DIR.joinpath("Stacking_clf.pkl")
        model = joblib.load(model_file_path)
        print(model.predict(data))
        return model.predict(data)

    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Predictor.objects.none()

        return Predictor.objects.filter(patient=profile)
