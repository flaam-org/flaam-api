import django_filters
from django.contrib.auth import get_user_model

from .models import Discussion, DiscussionComment

UserModel = get_user_model()


class DiscussionFilterSet(django_filters.FilterSet):
    owner_u = django_filters.CharFilter(
        field_name="owner__username",
        lookup_expr="iexact",
    )

    class Meta:
        model = Discussion
        fields = (
            "idea",
            "draft",
            "owner",
            "owner_u",
        )


class DiscussionCommentFilterSet(django_filters.FilterSet):

    discussion = django_filters.ModelChoiceFilter(
        queryset=Discussion.objects.all(),
        distinct=True,
    )

    owner_u = django_filters.CharFilter(
        field_name="owner__username",
        lookup_expr="iexact",
    )

    class Meta:
        model = DiscussionComment
        fields = (
            "discussion",
            "owner",
            "owner_u",
        )
