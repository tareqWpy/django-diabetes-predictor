from accounts.models import Profile, UserType
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from ...models import ReferralRelationship, ReferralToken
from .filters import ReferralRelationshipFilter, ReferralTokenFilter
from .paginations import DefaultPagination
from .permissions import IsAuthenticatedAndActive, IsDoctor
from .serializers import ReferralRelationshipSerializer, ReferralTokenSerializer


class ReferralTokenViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReferralTokenSerializer
    permission_classes = [IsAuthenticatedAndActive, IsDoctor]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReferralTokenFilter
    pagination_class = DefaultPagination
    search_fields = ["token"]
    ordering_fields = ["created_date"]
    lookup_field = "token"

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user.type in [UserType.doctor.value, UserType.superuser.value]:
            return ReferralToken.objects.filter(creator=profile).order_by(
                "created_date"
            )
        else:
            raise PermissionDenied(
                {"details": "Access denied: you must be a doctor to use this feature."}
            )


class ReferralRelationshipViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReferralRelationshipSerializer
    permission_classes = [IsAuthenticatedAndActive, IsDoctor]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReferralRelationshipFilter
    pagination_class = DefaultPagination
    search_fields = ["refer_token__token"]
    ordering_fields = ["created_date"]
    lookup_field = "refer_token"

    def get_object(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user.type in [UserType.doctor.value, UserType.superuser.value]:
            try:
                return ReferralRelationship.objects.get(
                    refer_from=profile,
                    refer_token__token=self.kwargs[self.lookup_field],
                )
            except ReferralRelationship.DoesNotExist:
                raise NotFound("Referral relationship not found.")
        else:
            raise PermissionDenied(
                {"details": "Access denied: you must be a doctor to use this feature."}
            )

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.user.type in [UserType.doctor.value, UserType.superuser.value]:
            return ReferralRelationship.objects.filter(refer_from=profile).order_by(
                "created_date"
            )
        else:
            raise PermissionDenied(
                {"details": "Access denied: you must be a doctor to use this feature."}
            )
