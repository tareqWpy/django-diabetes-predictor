from accounts.models import Profile, User, UserType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from pkg_resources import require
from rest_framework import serializers

from ...models import ReferralRelationship, ReferralToken


class UserInstanceSerializerRO(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "user_type",
        ]
        read_only_fields = ["id", "email", "user_type"]

    def get_user_type(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError(
                "You need to be logged in to update your profile."
            )
        return UserType(obj.type).label


class ReferralProfileInstanceSerializer(serializers.ModelSerializer):
    user = UserInstanceSerializerRO(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "created_date",
        ]
        read_only_fields = ["id", "user", "first_name", "last_name", "created_date"]


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
        read_only_fields = ["id", "creator", "token", "created_date"]

    def validate(self, attrs):
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

        return attrs


class ReferralTokenInstanceSerializer(serializers.ModelSerializer):
    creator = ReferralProfileInstanceSerializer(read_only=True)

    class Meta:
        model = ReferralToken
        fields = [
            "id",
            "creator",
            "token",
            "created_date",
        ]
        read_only_fields = ["id", "creator", "token", "created_date"]


class ReferralRelationshipSerializer(serializers.ModelSerializer):
    refer_from = ReferralProfileInstanceSerializer(read_only=True)
    refer_to = ReferralProfileInstanceSerializer(read_only=True)
    refer_token = ReferralTokenInstanceSerializer(read_only=True)

    class Meta:
        model = ReferralRelationship
        fields = ["id", "refer_from", "refer_to", "refer_token"]
