from django.shortcuts import get_object_or_404
from rest_framework import generics

from ...models import Profile
from .serializers import ProfileSerializer


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
