import os
from pathlib import Path

import joblib
import matplotlib
import sklearn
from django.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from ...models import Diabetes
from .serializers import PredictorSerializers


class PredictorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = PredictorSerializers
    queryset = Diabetes.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        scaled_data = self.preprocess_data(validated_data)
        result = self.get_prediction(scaled_data)

        predictor_instance = serializer.save(outcome=result)

        return Response(
            {
                "details": {
                    # returns result as a number
                    "outcome": result[0],
                    "id": predictor_instance.id,
                }
            },
            status=status.HTTP_201_CREATED,
        )

    def preprocess_data(self, data):
        scaler_file_path = settings.SERVICES_DIR.joinpath("scaler.pkl")
        scaler = joblib.load(scaler_file_path)
        features = [
            data["pregnancies"],
            data["glucose"],
            data["blood_pressure"],
            data["skin_thickness"],
            data["insulin"],
            data["bmi"],
            data["diabetes_pedigree_function"],
            data["age"],
        ]

        return scaler.transform([features])

    def get_prediction(self, data):
        model_file_path = settings.SERVICES_DIR.joinpath("model.pkl")
        model = joblib.load(model_file_path)
        result = model.predict(data)

        return result
