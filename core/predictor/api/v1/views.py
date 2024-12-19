import os
from pathlib import Path

import joblib
import sklearn
from django.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from ...models import Predictor
from .serializers import PredictorSerializers

# Set the SERVICES_DIR path to the "services" directory,
# which is located two levels up from the current directory.


class PredictorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = PredictorSerializers
    queryset = Predictor.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        scaled_data = self.preprocess_data(validated_data)
        result = self.get_prediction(scaled_data)

        predictor_instance = serializer.save(result=result)

        return Response(
            {
                "details": {
                    # returns result as a number
                    "result": result[0],
                    "id": predictor_instance.id,
                }
            },
            status=status.HTTP_201_CREATED,
        )

    def preprocess_data(self, data):
        scaler_file_path = settings.SERVICES_DIR.joinpath("scaler.pkl")
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

        return scaler.transform([features])

    def get_prediction(self, data):
        model_file_path = settings.SERVICES_DIR.joinpath("Stacking_clf.pkl")
        model = joblib.load(model_file_path)
        result = model.predict(data)

        return result
