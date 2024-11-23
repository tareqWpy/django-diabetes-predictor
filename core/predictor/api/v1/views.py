import os
from pathlib import Path

import joblib
import sklearn
from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from ...models import Predictor
from .paginations import DefaultPagination
from .permissions import IsAuthenticatedAndActive, IsPatient
from .serializers import PredictorSerializers

# Set the SERVICES_DIR path to the "services" directory,
# which is located two levels up from the current directory.
SERVICES_DIR = Path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "services")
)


class PredictorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for managing predictions made by patients.

    This ViewSet allows patients to create, retrieve, list, and delete prediction
    instances. It incorporates authentication and authorization checks to ensure
    that only valid users have access to create or view predictions.

    Attributes:
        serializer_class (Serializer): The serializer class used for validating
            and serializing prediction data.
        permission_classes (list): A list of permissions required for accessing
            the ViewSet, ensuring that users are authenticated and active.
        filter_backends (list): List of filter backends used for querying the
            Prediction instances.
        filterset_fields (dict): Fields available for filtering query results.
        search_fields (list): Fields available for search functionality.
        ordering_fields (list): Fields available for ordering query results.
        pagination_class (Pagination): The pagination class used for paginating
            the predictions list.

    Methods:
        create(request, *args, **kwargs): Validates the input data, processes it,
            and creates a new prediction instance, returning the result.
        preprocess_data(data): Scales input features using a pre-trained scaler
            for model prediction.
        get_prediction(data): Loads a pre-trained model and makes predictions
            based on the scaled data.
        get_queryset(): Retrieves the queryset of predictions based on the user's
            profile, ensuring that only authorized users can access their respective
            predictions.

    Raises:
        serializers.ValidationError: If the input data is not valid.
        PermissionDenied: If the user does not have the necessary permissions
            to access predictions.
    """

    permission_classes = [IsAuthenticatedAndActive, IsPatient]
    serializer_class = PredictorSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_fields = {
        "result": ["exact"],
        "patient": ["exact"],
        "created_date": ["gte", "lte"],
    }
    search_fields = ["result", "patient"]
    ordering_fields = ["created_date", "result"]

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

        if profile.user.type in {UserType.patient.value, UserType.superuser.value}:
            return Predictor.objects.filter(patient=profile)
        else:
            raise PermissionDenied(
                {
                    "details": "Access denied: you must be a patient or superuser to use this feature."
                }
            )
