import django_filters
from django.contrib.auth import get_user_model

from .models import Idea

UserModel = get_user_model()


class IdeaFilterSet(django_filters.FilterSet):

    bookmarked_by = django_filters.ModelChoiceFilter(
        field_name="bookmarked_by",
        queryset=UserModel.objects.all(),
        distinct=True,
    )

    owner_u = django_filters.CharFilter(
        field_name="owner__username",
        lookup_expr="iexact",
    )

    bookmarked_by_u = django_filters.CharFilter(
        field_name="bookmarked_by__username",
        lookup_expr="iexact",
    )

    class Meta:
        model = Idea
        fields = (
            "tags",
            "owner",
            "owner_u",
            "bookmarked_by",
            "bookmarked_by_u",
            "draft",
            "archived",
        )
