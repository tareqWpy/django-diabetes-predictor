from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ...models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
    password1 (CharField): The password entered by the user.
    """

    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        """
        Validates the password and ensures it matches the confirmation password.

        Args:
        attrs (dict): The attributes to be validated.

        Returns:
        dict: The validated attributes.

        Raises:
        ValidationError: If the passwords do not match or if the password does not meet the requirements.
        """
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"details": "Passwords must match."})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Creates a new user with the validated data.

        Args:
        validated_data (dict): The validated attributes.

        Returns:
        User: The newly created user.
        """
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)
