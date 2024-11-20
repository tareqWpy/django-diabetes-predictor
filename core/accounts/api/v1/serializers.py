from unittest.util import _MAX_LENGTH

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from djoser.serializers import PasswordRetypeSerializer, UserCreateMixin
from rest_framework import serializers
from rest_framework.settings import api_settings

from ...models import Profile, User, UserType


class UserInstanceSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "user_type")

    def get_user_type(self, obj):
        return UserType(obj.type).label


class RegistrationSerializer(UserCreateMixin, serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    type = serializers.ChoiceField(
        choices=[
            (UserType.patient.value, UserType.patient.label),
            (UserType.doctor.value, UserType.doctor.label),
        ],
        required=True,
        write_only=True,
    )
    first_name = serializers.CharField(max_length=255, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=255, allow_blank=True, required=False)
    referral_token = serializers.CharField(
        max_length=32, allow_blank=True, required=False
    )
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
            "first_name",
            "last_name",
            "type",
            "user_type",
            "password",
        )

    def get_user_type(self, obj):
        return UserType(obj.type).label

    def validate_type(self, value):
        if value not in [UserType.patient.value, UserType.doctor.value]:
            raise serializers.ValidationError(
                _("Invalid user type. Please select either 'patient' or 'doctor'."),
            )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        try:
            user = User(
                **{key: attrs[key] for key in User.REQUIRED_FIELDS if key in attrs}
            )
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
    user = UserInstanceSerializer(read_only=True)
    first_name = serializers.CharField(max_length=255, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ["id", "user", "first_name", "last_name", "image"]


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
