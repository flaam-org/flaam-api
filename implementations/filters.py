import django_filters
from django.contrib.auth import get_user_model

from .models import Implementation

UserModel = get_user_model()


class ImplementationFilterSet(django_filters.FilterSet):

    bookmarked_by = django_filters.ModelChoiceFilter(
        field_name="bookmarked_by",
        queryset=UserModel.objects.all(),
        distinct=True,
    )

    class Meta:
        model = Implementation
        fields = (
            "idea",
            "owner",
            "tags",
            "bookmarked_by",
            "draft",
            "is_validated",
            "is_accepted",
        )
