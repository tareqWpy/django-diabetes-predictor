from accounts.api.v1.serializers import ProfileSerializer, UserInstanceSerializer
from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import ReferralRelationship, ReferralToken
from ..utils import generate_unique_refer_token


class ReferralProfileInstanceSerializer(serializers.ModelSerializer):
    user = UserInstanceSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "created_date",
        ]
        read_only_fields = ["user", "created_date"]


class ReferralTokenInstanceSerializer(serializers.ModelSerializer):
    creator = ReferralProfileInstanceSerializer()

    class Meta:
        model = ReferralToken
        fields = [
            "id",
            "creator",
            "token",
            "created_date",
        ]
        read_only_fields = ["creator", "token", "created_date"]


class ReferralTokenSerializer(serializers.ModelSerializer):
    creator = ReferralProfileInstanceSerializer(read_only=True)

    class Meta:
        model = ReferralToken
        fields = [
            "id",
            "creator",
            "token",
            "first_name",
            "last_name",
            "created_date",
        ]
        read_only_fields = ["creator", "token", "created_date"]

    def create(self, validated_data):
        user = self.context["request"].user

        if user.is_anonymous:
            raise serializers.ValidationError(
                {"details": "User must be authenticated to create a Token."}
            )

        profile = get_object_or_404(Profile, user=user)

        if profile.user.type not in [UserType.doctor.value, UserType.superuser.value]:
            raise serializers.ValidationError(
                {
                    "details": "Access denied. Invalid user type, you must be a doctor or superuser."
                }
            )

        validated_data["creator"] = profile
        validated_data["token"] = generate_unique_refer_token()
        return super().create(validated_data)


class ReferralRelationshipSerializer(serializers.ModelSerializer):
    refer_from = ReferralProfileInstanceSerializer(read_only=True)
    refer_to = ReferralProfileInstanceSerializer(read_only=True)
    refer_token = ReferralTokenInstanceSerializer(read_only=True)

    class Meta:
        model = ReferralRelationship
        fields = ["id", "refer_from", "refer_to", "refer_token"]
