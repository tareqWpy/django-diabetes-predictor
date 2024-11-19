from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import ReferralToken
from ..utils import generate_unique_refer_token


class ReferralTokenSerializer(serializers.ModelSerializer):

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
