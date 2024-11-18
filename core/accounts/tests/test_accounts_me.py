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
def user_doctor_activated():
    """
    Creates and returns a common user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="doctor1@admin.com",
        password="9889taat",
        type=UserType.doctor.value,
        is_active=True,
    )
    return user


@pytest.mark.django_db
class TestAccountsMeAPI:
    """
    Test suite for 'GET' and 'DELETE' API endpoints related to 'me'.
    """

    def test_detele_account_response_400_status(
        self, api_client, user_doctor_activated
    ):
        """
        Test DELETE request to 'me' endpoint returns 400 status code.
        """
        url = reverse("accounts:api-v1:delete-account")
        user = user_doctor_activated

        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        print(response.status_code)
        print(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_account_response_204_status(
        self, api_client, user_doctor_activated
    ):
        """
        Test DELETE request to 'me' endpoint returns 204 status code.
        """
        url = reverse("accounts:api-v1:delete-account")
        data = {"current_password": "9889taat"}
        user = user_doctor_activated

        api_client.force_authenticate(user=user)
        response = api_client.delete(url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
