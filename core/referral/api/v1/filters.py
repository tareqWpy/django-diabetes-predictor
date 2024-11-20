from django_filters import rest_framework as filters

from ...models import ReferralRelationship, ReferralToken


class ReferralRelationshipFilter(filters.FilterSet):
    refer_token = filters.CharFilter(
        field_name="refer_token__token", lookup_expr="icontains"
    )

    class Meta:
        model = ReferralRelationship
        fields = {
            "created_date": ["gte", "lte"],
        }


class ReferralTokenFilter(filters.FilterSet):
    token = filters.CharFilter(field_name="token", lookup_expr="icontains")

    class Meta:
        model = ReferralToken
        fields = {
            "created_date": ["gte", "lte"],
        }
