from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from ...models import ReferralToken
from .paginations import DefaultPagination
from .permissions import IsAuthenticatedAndActive
from .serializers import ReferralTokenSerializer


class ReferralViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReferralTokenSerializer
    permission_classes = [IsAuthenticatedAndActive]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "token": ["exact"],
        "creator": ["exact"],
        "created_date": ["gte", "lte"],
    }
    search_fields = ["token"]
    ordering_fields = ["created_date"]
    pagination_class = DefaultPagination
    lookup_field = "token"

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user.type in [UserType.doctor.value, UserType.superuser.value]:
            return ReferralToken.objects.filter(creator=profile)
        else:
            raise PermissionDenied(
                {"details": "Access denied: you must be a doctor to use this feature."}
            )
