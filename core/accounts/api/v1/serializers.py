from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from djoser.serializers import PasswordRetypeSerializer, UserCreateMixin
from rest_framework import serializers
from rest_framework.settings import api_settings

from ...models import Profile, User, UserType


class RegistrationSerializer(UserCreateMixin, serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=[
            (UserType.patient.value, UserType.patient.label),
            (UserType.doctor.value, UserType.doctor.label),
        ],
        required=True,
    )

    referral_token = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "referral_token",
            "type",
            "password",
        )

    def validate_type(self, value):
        if value not in [UserType.patient.value, UserType.doctor.value]:
            raise serializers.ValidationError(
                _("Invalid user type. Please select either 'patient' or 'doctor'."),
            )
        return value

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs


class UserCreatePasswordRetypeSerializer(RegistrationSerializer):
    default_error_messages = {
        "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "image"]


class AccountDeleteSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    class Meta:
        model = User
        fields = ["current_password"]
