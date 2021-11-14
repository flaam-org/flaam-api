import django_filters
from django.contrib.auth import get_user_model

from .models import Implementation, ImplementationComment

UserModel = get_user_model()


class ImplementationFilterSet(django_filters.FilterSet):

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
        model = Implementation
        fields = (
            "idea",
            "owner",
            "owner_u",
            "bookmarked_by",
            "bookmarked_by_u",
            "draft",
            "is_validated",
            "is_accepted",
        )


class ImplementationCommentFilterSet(django_filters.FilterSet):

    implementation = django_filters.ModelChoiceFilter(
        field_name="implementation",
        queryset=Implementation.objects.all(),
        distinct=True,
    )

    bookmarked_by = django_filters.ModelChoiceFilter(
        field_name="bookmarked_by",
        queryset=UserModel.objects.all(),
        distinct=True,
    )

    owner_u = django_filters.CharFilter(
        field_name="owner__username",
        lookup_expr="iexact",
    )

    class Meta:
        model = ImplementationComment
        fields = ("implementation", "owner", "owner_u")
