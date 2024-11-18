from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from predictor.api.v1.permissions import IsAuthenticatedAndActive
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models import Profile, User
from .serializers import AccountDeleteSerializer, ProfileSerializer


class ProfileAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class CustomUserViewSet(UserViewSet):
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)


class AccountDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = AccountDeleteSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
