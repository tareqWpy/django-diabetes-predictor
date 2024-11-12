from accounts.models import Profile, User
from django.urls import reverse
from rest_framework import serializers

from ...models import Patient, PredictionByDoctor, Predictor


class PredictorSerializers(serializers.ModelSerializer):
    """Serializer Class for Predictor model instances.

    This serializer handles the serialization and deserialization of
    Predictor model instances, providing additional fields for API URLs.

    Attributes:
        relative_url (URLField): A read-only field that provides the relative API URL.
        absolute_url (SerializerMethodField): A method field that returns the absolute URL
            of the predictor instance.

    Raises:
        serializers.ValidationError: Raised when a user attempts to create a predictor
            without proper authentication.
        serializers.ValidationError: Raised when the authenticated user does not have
            an associated profile in the system.

    Returns:
        dict: A representation of the predictor instance, including all specified fields
              and URLs, suitable for use in API responses.
    """

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Predictor
        fields = [
            "id",
            "patient",
            "female_age",
            "AMH",
            "FSH",
            "no_embryos",
            "endoendometerial_tickness",
            "sperm_count",
            "sperm_morphology",
            "follicle_size",
            "no_of_retreived_oocytes",
            "qality_of_embryo",
            "quality_of_retreived_oocytes_MI",
            "quality_of_retreived_oocytes_MII",
            "result",
            "relative_url",
            "absolute_url",
            "created_date",
        ]
        read_only_fields = ["patient", "result"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("predictor:api-v1:predictor-detail", args=[obj.pk])
        )

    def to_representation(self, obj):
        request = self.context.get("request")
        rep = super().to_representation(obj)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)

        return rep

    def create(self, validated_data):
        user = self.context["request"].user

        if user.is_anonymous:
            raise serializers.ValidationError(
                "User must be authenticated to create a predictor."
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")

        validated_data["patient"] = profile
        return super().create(validated_data)


class DoctorPredictorSerializers(serializers.ModelSerializer):

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = PredictionByDoctor
        fields = [
            "id",
            "doctor",
            "patient",
            "female_age",
            "AMH",
            "FSH",
            "no_embryos",
            "endoendometerial_tickness",
            "sperm_count",
            "sperm_morphology",
            "follicle_size",
            "no_of_retreived_oocytes",
            "qality_of_embryo",
            "quality_of_retreived_oocytes_MI",
            "quality_of_retreived_oocytes_MII",
            "result",
            "relative_url",
            "absolute_url",
            "created_date",
        ]
        read_only_fields = ["doctor", "result"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("predictor:api-v1:doctor-detail", args=[obj.pk])
        )

    def to_representation(self, obj):
        request = self.context.get("request")
        rep = super().to_representation(obj)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)

        return rep

    def create(self, validated_data):
        user = self.context["request"].user

        if user.is_anonymous:
            raise serializers.ValidationError(
                "User must be authenticated to create a predictor."
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")

        validated_data["doctor"] = profile
        return super().create(validated_data)


class PatientSerializers(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            "id",
            "manager",
            "first_name",
            "last_name",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["manager"]
