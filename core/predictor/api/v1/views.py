import os
from pathlib import Path

import joblib
import sklearn
from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from ...models import DoctorPredictor, Patient, PatientPredictor
from .paginations import DefaultPagination
from .permissions import IsAuthenticatedAndActive
from .serializers import (
    ClientPredictorSerializers,
    DoctorPredictorSerializers,
    PatientSerializers,
)

# Set the SERVICES_DIR path to the "services" directory,
# which is located two levels up from the current directory.
SERVICES_DIR = Path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "services")
)


class PredictionByClientViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for managing Prediction by Client model instances.

    This ViewSet provides operations to create, retrieve, list, and delete
    Predictor model entries. It includes functionality for processing input data,
    making predictions using a trained machine learning model, and returning the
    results.

    Args:
        mixins.CreateModelMixin: Mixin that provides create operation.
        mixins.RetrieveModelMixin: Mixin that provides retrieve operation.
        mixins.DestroyModelMixin: Mixin that provides delete operation.
        mixins.ListModelMixin: Mixin that provides list operation.
        viewsets.GenericViewSet: Base class for creating generic viewsets.

    Attributes:
        permission_classes (list): A list of permissions that the view requires.
        serializer_class (type): The serializer class used for input and output.
        filter_backends (list): A list of backends used for filtering querysets.
        filterset_fields (dict): Fields and their lookup expressions for filtering.
        ordering_fields (list): Fields that can be used for ordering the results.
        pagination_class (type): The pagination class for paginating results.

    Returns:
        Response: A Django Rest Framework Response object containing the result
            of the operations performed (e.g., created instance, retrieved
            instance, etc.).

    Methods:
        create(request, *args, **kwargs): Handles creation of a new Predictor entry.
        preprocess_data(data): Scales input features for prediction.
        get_prediction(data): Makes a prediction based on the processed data.
        get_queryset(): Retrieves a queryset of Predictor instances for the authenticated user.
    """

    premission_class = [IsAuthenticatedAndActive]
    serializer_class = ClientPredictorSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {"result": ["exact"], "created_date": ["gte", "lte"]}
    search_fields = ["result"]
    ordering_fields = ["created_date", "result"]
    pagination_class = DefaultPagination

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

        return scaler.transform([features])

    def get_prediction(self, data):
        model_file_path = SERVICES_DIR.joinpath("Stacking_clf.pkl")
        model = joblib.load(model_file_path)
        result = model.predict(data)

        return result

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user_type in {UserType.client, UserType.superuser}:
            return PatientPredictor.objects.filter(client=profile)
        else:
            raise PermissionDenied(
                {
                    "details": "Access denied: you must be a client or superuser to use this feature."
                }
            )


class PredictionByDoctorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for managing Prediction by Doctor model instances.

    This ViewSet provides operations to create, retrieve, list, and delete
    Predictor model entries. It includes functionality for processing input data,
    making predictions using a trained machine learning model, and returning the
    results.

    Args:
        mixins.CreateModelMixin: Mixin that provides create operation.
        mixins.RetrieveModelMixin: Mixin that provides retrieve operation.
        mixins.DestroyModelMixin: Mixin that provides delete operation.
        mixins.ListModelMixin: Mixin that provides list operation.
        viewsets.GenericViewSet: Base class for creating generic viewsets.

    Attributes:
        permission_classes (list): A list of permissions that the view requires.
        serializer_class (type): The serializer class used for input and output.
        filter_backends (list): A list of backends used for filtering querysets.
        filterset_fields (dict): Fields and their lookup expressions for filtering.
        ordering_fields (list): Fields that can be used for ordering the results.
        pagination_class (type): The pagination class for paginating results.

    Returns:
        Response: A Django Rest Framework Response object containing the result
            of the operations performed (e.g., created instance, retrieved
            instance, etc.).

    Methods:
        create(request, *args, **kwargs): Handles creation of a new Predictor entry.
        preprocess_data(data): Scales input features for prediction.
        get_prediction(data): Makes a prediction based on the processed data.
        get_queryset(): Retrieves a queryset of Predictor instances for the authenticated user.
    """

    serializer_class = DoctorPredictorSerializers
    premission_class = [IsAuthenticatedAndActive]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "result": ["exact"],
        "patient": ["exact"],
        "created_date": ["gte", "lte"],
    }
    search_fields = ["result", "patient"]
    ordering_fields = ["created_date", "result"]
    pagination_class = DefaultPagination

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

        return scaler.transform([features])

    def get_prediction(self, data):
        model_file_path = SERVICES_DIR.joinpath("Stacking_clf.pkl")
        model = joblib.load(model_file_path)
        result = model.predict(data)

        return result

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user_type in {UserType.doctor, UserType.superuser}:
            return DoctorPredictor.objects.filter(doctor=profile)
        else:
            raise PermissionDenied(
                {
                    "details": "Access denied: you must be a doctor or superuser to use this feature."
                }
            )


class PatientModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """A ViewSet for managing patient records."""

    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = PatientSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "id": ["iexact"],
        "first_name": ["iexact", "istartswith"],
        "last_name": ["iexact", "istartswith"],
        "created_date": ["gte", "lte"],
    }
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user_type in {UserType.doctor, UserType.superuser}:
            return Patient.objects.filter(manager=profile)

        raise PermissionDenied(
            detail="Access denied: you must be a doctor or superuser to use this feature."
        )

    def perform_create(self, serializer):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(manager=profile)
