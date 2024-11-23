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


@pytest.fixture
def refer_token_create_without_names(api_client, user_doctor_active):
    """
    Creates and returns a token for testing API endpoints.
    """
    url = reverse("referral:api-v1:referral-list")
    user = user_doctor_active
    api_client.force_authenticate(user=user)
    response = api_client.post(url)
    id = response.data["id"]
    creator = response.data["creator"]
    token = response.data["token"]
    return (
        id,
        creator,
        token,
    )


@pytest.fixture
def refer_token_create_with_names(api_client, user_doctor_active):
    """
    Creates and returns a token for testing API endpoints.
    """
    url = reverse("referral:api-v1:referral-list")
    user = user_doctor_active
    api_client.force_authenticate(user=user)
    data = {"first_name": "John", "last_name": "Doe"}
    response = api_client.post(url, data=data)
    id = response.data["id"]
    creator = response.data["creator"]
    token = response.data["token"]
    first_name = response.data["first_name"]
    last_name = response.data["last_name"]
    return id, creator, token, first_name, last_name


@pytest.mark.django_db
class TestReferralAPI:
    """
    Test suite for referral app endpoints.
    """

    """
    ########## referral:api-v1:referral-list ##########
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
        assert "first_name" in response.data
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

    ########## referral:api-v1:referral-detail ##########

    def test_doctor_active_get_referral_token_detail_without_names_200_status(
        self, api_client, user_doctor_active, refer_token_create_without_names
    ):
        id, creator, token = refer_token_create_without_names
        url = reverse("referral:api-v1:referral-detail", kwargs={"token": token})
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["creator"]["user"]["email"] == user.email
        assert (
            response.data["creator"]["user"]["user_type"]
            == user.user_type
            == UserType.doctor.label
        )
        assert "first_name" in response.data
        assert response.data["first_name"] == None
        assert "last_name" in response.data
        assert response.data["last_name"] == None

    def test_doctor_active_get_referral_token_detail_with_names_200_status(
        self, api_client, user_doctor_active, refer_token_create_with_names
    ):
        id, creator, token, first_name, last_name = refer_token_create_with_names
        url = reverse("referral:api-v1:referral-detail", kwargs={"token": token})
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["creator"]["user"]["email"] == user.email
        assert (
            response.data["creator"]["user"]["user_type"]
            == user.user_type
            == UserType.doctor.label
        )
        assert "first_name" in response.data
        assert response.data["first_name"] == "John"
        assert "last_name" in response.data
        assert response.data["last_name"] == "Doe"

    def test_patient_active_get_referral_token_403_status(
        self, api_client, user_patient_active, refer_token_create_without_names
    ):
        id, creator, token = refer_token_create_without_names
        url = reverse("referral:api-v1:referral-detail", kwargs={"token": token})
        user = user_patient_active
        api_client.force_authenticate(user=user)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doctor_active_delete_referral_token_204_status(
        self, api_client, user_doctor_active, refer_token_create_without_names
    ):
        id, creator, token = refer_token_create_without_names
        url = reverse("referral:api-v1:referral-detail", kwargs={"token": token})
        user = user_doctor_active
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_patient_active_delete_referral_token_403_status(
        self, api_client, user_patient_active, refer_token_create_without_names
    ):
        id, creator, token = refer_token_create_without_names
        url = reverse("referral:api-v1:referral-detail", kwargs={"token": token})
        user = user_patient_active
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    """

    ########## referral:api-v1:get-relations-list ##########
    # def test_get_referral_relation_lisr_with_names_status_200(
    #     self, api_client, user_doctor_active, refer_token_create_with_names
    # ):
    #     url = reverse("referral:api-v1:get-relations-list")
    #     user_doctor = user_doctor_active
    #     id, creator, token, first_name, last_name = refer_token_create_with_names

    #     # creating a user based on a referral token created by doctor
    #     user_patient = User.objects.create_user(
    #         email="patient1@admin.com",
    #         password="9889taat",
    #         referral_token=token,
    #         first_name=first_name,
    #         last_name=last_name,
    #         type=UserType.patient.value,
    #         is_active=True,
    #     )

    #     # loging in with doctor user
    #     api_client.force_authenticate(user=user_doctor)
    #     response = api_client.get(url)
    #     print(response.data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert "refer_from" in response.data["results"][0]
    #     assert "refer_to" in response.data["results"][0]
    #     assert "refer_token" in response.data["results"][0]
    #     assert (
    #         response.data["results"][0]["refer_from"]["user"]["email"]
    #         == user_doctor.email
    #     )
    #     assert (
    #         response.data["results"][0]["refer_from"]["user"]["user_type"]
    #         == user_doctor.user_type
    #         == UserType.doctor.label
    #     )
    #     assert (
    #         response.data["results"][0]["refer_from"]["user"]["email"]
    #         == creator["user"]["email"]
    #     )
    #     assert (
    #         response.data["results"][0]["refer_from"]["user"]["user_type"]
    #         == creator["user"]["user_type"]
    #     )
    #     assert (
    #         response.data["results"][0]["refer_to"]["user"]["email"]
    #         == user_patient.email
    #     )
    #     assert (
    #         response.data["results"][0]["refer_to"]["user"]["user_type"]
    #         == user_patient.user_type
    #         == UserType.patient.label
    #     )
    #     assert response.data["results"][0]["refer_to"]["first_name"] == first_name
    #     assert response.data["results"][0]["refer_to"]["last_name"] == last_name
    #     assert response.data["results"][0]["refer_token"]["token"] == token
    #     assert response.data["results"][0]["refer_token"]["creator"] == creator

    # def test_get_referral_relatio_status_401(self, api_client):
    #     url = reverse("referral:api-v1:get-relations-list")

    #     response = api_client.get(url)
    #     print(response.data)
    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_get_referral_relation_patient_status_403(
    #     self, api_client, user_patient_active
    # ):
    #     url = reverse("referral:api-v1:get-relations-list")

    #     api_client.force_authenticate(user=user_patient_active)
    #     response = api_client.get(url)
    #     print(response.data)
    #     assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_referral_relation_detail_with_names_status_200(
        self, api_client, user_doctor_active, refer_token_create_with_names
    ):
        user_doctor = user_doctor_active
        id, creator, token, first_name, last_name = refer_token_create_with_names
        refer_token = id
        url = reverse(
            "referral:api-v1:get-relations-detail", kwargs={"refer_token": refer_token}
        )

        # creating a user based on a referral token created by doctor
        user_patient = User.objects.create_user(
            email="patient1@admin.com",
            password="9889taat",
            referral_token=token,
            first_name=first_name,
            last_name=last_name,
            type=UserType.patient.value,
            is_active=True,
        )

        # loging in with doctor user
        api_client.force_authenticate(user=user_doctor)
        response = api_client.get(url)
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
