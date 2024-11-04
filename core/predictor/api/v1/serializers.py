from accounts.models import Profile, User
from django.urls import reverse
from rest_framework import serializers

from ...models import Predictor


class PredictorSerializers(serializers.ModelSerializer):
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
            "endoendometrial_thickness",
            "sperm_count",
            "sperm_morphology",
            "follicle_size",
            "retrieved_oocytes",
            "quality_of_embryo",
            "retrieved_oocytes_MI",
            "retrieved_oocytes_MII",
            "relative_url",
            "absolute_url",
            "created_date",
        ]
        read_only_fields = ["patient"]

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
        else:
            rep.pop("updated_date", None)

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
