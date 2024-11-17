from accounts.models import Profile, UserType
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import Predictor


class PredictorSerializers(serializers.ModelSerializer):
    """
    Serializer for the Predictor model.

    This serializer manages the transformation of Predictor model instances
    into JSON format and vice versa. It includes fields for patient attributes,
    various health measurements, and endpoints for API access.

    Attributes:
        relative_url (URLField): A read-only field generating the relative URL
            for the Predictor instance.
        absolute_url (SerializerMethodField): A read-only field generating the
            absolute URL for the Predictor instance.

    Meta:
        model (Predictor): The model class to be serialized.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): Fields that should not be writable by users.

    Methods:
        get_abs_url(obj): Constructs the absolute URL for the instance.
        to_representation(obj): Customizes the representation for the serializer,
            removing URL fields based on the request context.
        create(validated_data): Handles the creation of a new Predictor
            instance, validating user authentication,type and profile existence.

    Raises:
        serializers.ValidationError: If the user is not authenticated, the profile
        does not exist, or related patient cannot be found.
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
        read_only_fields = ["patient", "result", "created_date"]

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
                {"details": "User must be authenticated to create a predictor."}
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {"details": "Profile does not exist for this user."}
            )

        # Check if the user type is valid
        if profile.user.type not in [UserType.patient.value, UserType.superuser.value]:
            raise serializers.ValidationError(
                {"details": "Access denied. Invalid user type, you must be a patient."}
            )

        validated_data["patient"] = profile
        return super().create(validated_data)
