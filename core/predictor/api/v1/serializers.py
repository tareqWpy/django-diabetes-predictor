from accounts.models import Profile, User
from django.urls import reverse
from rest_framework import serializers

from ...models import DoctorPredictor, Patient, PatientPredictor


class ClientPredictorSerializers(serializers.ModelSerializer):
    """Serializer Class for Predictor model instances.

    This serializer handles the serialization and deserialization of
    Predictor model instances, providing additional fields for API URLs.
    """

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = PatientPredictor
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
        read_only_fields = ["client", "result"]

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
                "User must be authenticated to create a predictor."
            )

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile does not exist for this user.")

        validated_data["client"] = profile
        return super().create(validated_data)


class DoctorPredictorSerializers(serializers.ModelSerializer):

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
        read_only_fields = ["doctor", "result"]

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

        validated_data["doctor"] = profile

        instance = super().create(validated_data)

        if not Patient.objects.filter(id=instance.patient.id, manager=profile).exists():
            raise serializers.ValidationError(
                "This patient does not exist for this user."
            )

        return instance


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
