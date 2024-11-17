import secrets

from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import Referral
from ..utils import generate_unique_refer_token


class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
        fields = [
            "id",
            "refer_from",
            "refer_to",
            "refer_token",
            "is_expired",
            "created_date",
        ]
        read_only_fields = ["refer_from", "refer_token", "created_date"]

    def create(self, validated_data):
        user = self.context["request"].user

        if user.is_anonymous:
            raise serializers.ValidationError(
                {"details": "User must be authenticated to create a Token."}
            )

        profile = get_object_or_404(Profile, user=user)

        if profile.user.type not in [UserType.doctor.value, UserType.superuser.value]:
            raise serializers.ValidationError(
                {"details": "Access denied. Invalid user type, you must be a doctor."}
            )

        validated_data["refer_from"] = profile
        validated_data["refer_token"] = generate_unique_refer_token()
        return super().create(validated_data)
