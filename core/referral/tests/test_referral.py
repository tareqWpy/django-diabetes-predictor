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
        is_active=False,
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
        is_active=False,
    )
    return user


@pytest.mark.django_db
class TestAccountsMeAPI:
    """
    Test suite for referral app endpoints.
    """

    def test_doctor_active_get_referral_token_list_200_status(
        self, api_client, user_doctor_active
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_patien_active_get_referral_token_list_403_status(
        self, api_client, user_patient_active
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_patient_active
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doctor_active_post_referral_token_list_without_credentials_201_status(
        self, api_client, user_doctor_active
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data
        assert "creator" in response.data
        assert response.data["first_name"] == None
        assert "last_name" in response.data
        assert response.data["last_name"] == None

    def test_doctor_active_post_referral_token_list_with_credentials_201_status(
        self, api_client, user_doctor_active
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data={"first_name": "John", "last_name": "Doe"})

        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data
        assert "creator" in response.data
        assert "first_name" in response.data
        assert response.data["first_name"] == "John"
        assert "last_name" in response.data
        assert response.data["last_name"] == "Doe"

    def test_patient_active_post_referral_token_list_403_status(
        self, api_client, user_patient_active
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_patient_active
        api_client.force_authenticate(user=user)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doctor_inactive_get_referral_token_list_403_status(
        self, api_client, user_doctor_inactive
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_doctor_inactive
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), '{"detail": "Authentication credentials were not provided."}'

    def test_patient_inactive_post_referral_token_list_403_status(
        self, api_client, user_patient_inactive
    ):
        url = reverse("referral:api-v1:referral-list")
        user = user_patient_inactive
        api_client.force_authenticate(user=user)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
