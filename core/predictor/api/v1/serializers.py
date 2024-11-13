from accounts.models import Profile, User, UserType
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import ClientPredictor, DoctorPredictor, Patient


class ClientPredictorSerializers(serializers.ModelSerializer):
    """
    Serializer for the ClientPredictor model.

    This serializer manages the transformation of ClientPredictor model instances
    into JSON format and vice versa. It includes fields for client attributes,
    various health measurements, and endpoints for API access.

    Attributes:
        relative_url (URLField): A read-only field generating the relative URL
            for the ClientPredictor instance.
        absolute_url (SerializerMethodField): A read-only field generating the
            absolute URL for the ClientPredictor instance.

    Meta:
        model (ClientPredictor): The model class to be serialized.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): Fields that should not be writable by users.

    Methods:
        get_abs_url(obj): Constructs the absolute URL for the instance.
        to_representation(obj): Customizes the representation for the serializer,
            removing URL fields based on the request context.
        create(validated_data): Handles the creation of a new ClientPredictor
            instance, validating user authentication,type and profile existence.

    Raises:
        serializers.ValidationError: If the user is not authenticated, the profile
        does not exist, or related client cannot be found.
    """

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = ClientPredictor
        fields = [
            "id",
            "client",
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
        read_only_fields = ["client", "result", "created_date"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("predictor:api-v1:client-predictor-detail", args=[obj.pk])
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
                _("User must be authenticated to create a predictor.")
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                _("Profile does not exist for this user.")
            )

        # Check if the user type is valid
        if profile.user_type not in [UserType.client.value]:
            raise serializers.ValidationError(
                _("Access denied. Invalid user type, you must be a client.")
            )

        validated_data["client"] = profile
        return super().create(validated_data)


class DoctorPredictorSerializers(serializers.ModelSerializer):
    """
    Serializer for the DoctorPredictor model.

    This serializer handles the conversion of DoctorPredictor model instances
    into JSON format and vice versa. It includes fields for doctor and patient
    details, various medical measurements, and URLs for accessing API endpoints.

    Attributes:
        relative_url (URLField): A read-only field generating the relative URL
            for the DoctorPredictor instance.
        absolute_url (SerializerMethodField): A read-only field generating the
            absolute URL for the DoctorPredictor instance.

    Meta:
        model (DoctorPredictor): The model class to be serialized.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): Fields that should not be writable by users.

    Methods:
        get_abs_url(obj): Constructs the absolute URL for the instance.
        to_representation(obj): Customizes the representation for the serializer,
            removing URL fields based on the request context.
        create(validated_data): Handles the creation of a new DoctorPredictor
            instance, validating user authentication,type and profile existence.

    Raises:
        serializers.ValidationError: If the user is not authenticated, profile
        does not exist, or related patient cannot be found.
    """

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = DoctorPredictor
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
        read_only_fields = ["doctor", "result", "created_date"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("predictor:api-v1:doctor-predictor-detail", args=[obj.pk])
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

        if profile.user_type not in [UserType.doctor.value]:
            raise serializers.ValidationError(
                _("Access denied. Invalid user type, you must be a doctor.")
            )

        validated_data["doctor"] = profile
        instance = super().create(validated_data)

        if not Patient.objects.filter(id=instance.patient.id, manager=profile).exists():
            raise serializers.ValidationError(
                "The patient does not exist for this user."
            )

        return instance


class PatientSerializers(serializers.ModelSerializer):
    """
    Serializer for the Patient model.

    This serializer handles the conversion of Patient model instances
    into JSON format and vice versa. It includes fields for patient
    details, such as the patient's name and timestamps, as well as
    URLs for accessing API endpoints.

    Attributes:
        relative_url (URLField): A read-only field generating the relative URL
            for the Patient instance.
        absolute_url (SerializerMethodField): A read-only field generating the
            absolute URL for the Patient instance.

    Meta:
        model (Patient): The model class to be serialized.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): Fields that should not be writable by users.

    Methods:
        get_abs_url(obj): Constructs the absolute URL for the instance.
        to_representation(obj): Customizes the representation for the serializer,
            removing URL fields based on the request context.
        create(validated_data): Handles the creation of a new Patient instance,
            validating user authentication and profile existence.

    Raises:
        serializers.ValidationError: If the user is not authenticated, profile
        does not exist, or if any other validation errors occur.
    """

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Patient
        fields = [
            "id",
            "manager",
            "first_name",
            "last_name",
            "created_date",
            "updated_date",
            "relative_url",
            "absolute_url",
        ]
        read_only_fields = ["manager", "created_date", "updated_date"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("predictor:api-v1:patient-detail", args=[obj.pk])
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
                "User must be authenticated to create a patient."
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")

        if profile.user_type not in [UserType.doctor.value]:
            raise serializers.ValidationError(
                _("Access denied. Invalid user type, you must be a doctor.")
            )

        validated_data["manager"] = profile

        return super().create(validated_data)
