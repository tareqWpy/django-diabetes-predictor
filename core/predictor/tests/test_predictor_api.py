import pytest
from accounts.models import User
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
def common_user():
    """
    Creates and returns a common user for testing API endpoints.
    """
    user = User.objects.create_user(
        email="admin@admin.com", password="123456789@", is_active=True
    )
    return user


@pytest.fixture
def client_input_data():
    """
    Returns a sample of data for testing API endpoints, using common_user fixture.
    """
    input_data = {
        "female_age": 37,
        "AMH": "2",
        "FSH": "1",
        "no_embryos": 5,
        "endoendometerial_tickness": "8",
        "sperm_count": "36",
        "sperm_morphology": 3,
        "follicle_size": 18,
        "no_of_retreived_oocytes": 16,
        "qality_of_embryo": 7,
        "quality_of_retreived_oocytes_MI": 0,
        "quality_of_retreived_oocytes_MII": 12,
    }

    return input_data


@pytest.fixture
def doctor_input_data():
    """
    Returns a sample of data for testing API endpoints, using common_user fixture.
    """
    input_data = {
        "female_age": 37,
        "AMH": "2",
        "FSH": "1",
        "no_embryos": 5,
        "endoendometerial_tickness": "8",
        "sperm_count": "36",
        "sperm_morphology": 3,
        "follicle_size": 18,
        "no_of_retreived_oocytes": 16,
        "qality_of_embryo": 7,
        "quality_of_retreived_oocytes_MI": 0,
        "quality_of_retreived_oocytes_MII": 12,
    }

    return input_data


@pytest.fixture
def common_prediction_id(api_client, common_user, sample_input_data):
    """
    Returns a common prediction id of data for testing API endpoints, using api_client, common_user, sample_input_data fixture.
    """
    url = reverse("predictor:api-v1:predictor-list")
    user = common_user
    api_client.force_authenticate(user=user)

    response = api_client.post(url, sample_input_data)
    prediction_id = response.data["details"]["id"]

    return prediction_id


@pytest.mark.django_db
class TestPredictorAPI:
    """
    Test suite for GET, POST, DELETE API endpoints related to Predictor.
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
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_prediction_response_204_status(
        self, api_client, common_prediction_id
    ):
        """
        Test DELETE request to predictor Instance endpoint returns 204 status code.
        """

        delete_url = reverse(
            "predictor:api-v1:predictor-detail",
            args=[common_prediction_id],
        )
        response = api_client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_detail_prediction_response_200_status(
        self, api_client, common_prediction_id
    ):
        """
        Test GET request to predictor Instance endpoint returns 200 status code.
        """
        delete_url = reverse(
            "predictor:api-v1:predictor-detail", args=[common_prediction_id]
        )
        response = api_client.get(delete_url)

        assert response.status_code == status.HTTP_200_OK
