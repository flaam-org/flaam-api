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

    class Meta:
        model = Idea
        fields = (
            "owner",
            "tags",
            "bookmarked_by",
            "draft",
        )
