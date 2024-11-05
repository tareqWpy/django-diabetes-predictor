from django.shortcuts import get_object_or_404
from rest_framework import generics

from ...models import Profile
from .serializers import ProfileSerializer


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
