import pytest
from accounts.models import User, UserType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Returns an instance of APIClient for testing API endpoints.
    """
    client = APIClient()
    return client


@pytest.fixture
def user_doctor_active():
    """
    Creates and returns a active doctor user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="doctor1@admin.com",
        password="9889taat",
        type=UserType.doctor.value,
        is_active=True,
    )
    return user


@pytest.fixture
def user_doctor_inactive():
    """
    Creates and returns a inactive doctor user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="doctor1@admin.com",
        password="9889taat",
        type=UserType.doctor.value,
        is_active=True,
    )
    return user


@pytest.fixture
def user_patient_active():
    """
    Creates and returns a active patient user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="patient1@admin.com",
        password="9889taat",
        type=UserType.patient.value,
        is_active=True,
    )
    return user


@pytest.fixture
def user_patient_inactive():
    """
    Creates and returns a inactive patient user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="patient1@admin.com",
        password="9889taat",
        type=UserType.patient.value,
        is_active=True,
    )
    return user


@pytest.mark.django_db
class TestAccountsMeAPI:
    """
    Test suite for 'GET' and 'DELETE' API endpoints related to 'me'.
    """

    def test_post_referral_token_empty_input_200_status(self, api_client, user_doctor_active):
        """
        Test DELETE request to 'me' endpoint returns 400 status code.
        """
        url = reverse("referral:api-v1:referral")
        user = user_doctor_active

        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), '{"current_password": ["This field is required."]}'
