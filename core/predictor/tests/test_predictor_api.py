import pytest
from accounts.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Predictor


@pytest.fixture
def api_client():
    """
    Returns an instance of APIClient for testing API endpoints.
    """
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    """
    Creates and returns a common user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="admin@admin.com", password="123456789@", is_active=True
    )
    return user


@pytest.fixture
def sample_input_data():
    """
    Returns a sample of data for testing API endpoints, using common_user fixture.
    """
    input_data = {
        "female_age": 30,
        "AMH": 2.50,
        "FSH": 5.00,
        "no_embryos": 3,
        "endometrial_thickness": 8.0,
        "sperm_count": 20.0,
        "sperm_morphology": 4.0,
        "follicle_size": 18.0,
        "no_of_retrieved_oocytes": 10,
        "quality_of_embryo": 8.0,
        "quality_of_retrieved_oocytes_MI": 9.0,
        "quality_of_retrieved_oocytes_MII": 10.0,
    }

    return input_data


@pytest.mark.django_db
class TestPredictorAPI:
    """
    Test suite for POST API endpoints related to Predictor.
    """

    def test_get_prediction_list_response_200_status(self, api_client, common_user):
        """
        Test GET request to predictor list endpoint returns 200 status code.
        """
        url = reverse("predictor:api-v1:predictor-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_prediction_response_201_status(
        self, api_client, common_user, sample_input_data
    ):
        """
        Test POST request to predictor Instance endpoint returns 200 status code.
        """
        url = reverse("predictor:api-v1:predictor-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, sample_input_data)
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
