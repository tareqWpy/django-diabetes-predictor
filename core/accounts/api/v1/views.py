from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from ...models import Profile, UserType
from .serializers import ProfileSerializer

User = get_user_model()


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile information.

    This view inherits from Django Rest Framework's RetrieveUpdateAPIView,
    which provides a default implementation for GET (retrieve) and PATCH/PUT
    (update) actions. It handles operations for the Profile model specifically
    for the currently authenticated user.

    Attributes:
        serializer_class (ProfileSerializer): The serializer used to validate
            and serialize the profile data.
        queryset (QuerySet): A queryset that retrieves all Profile instances.

    Methods:
        get_object():
            Retrieves the profile object for the currently authenticated user.
            If the profile does not exist, raises a 404 error.

    Usage:
        - To retrieve the profile, send a GET request to the endpoint.
        - To update the profile, send a PATCH or PUT request with the new
          profile data.

    Note:
        This view assumes the user is authenticated and has a corresponding
        Profile object. The view uses the request user strictly for
        profile lookups.
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class CustomUserViewSet(UserViewSet):

    @action(["get", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        user = self.get_object()

        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
