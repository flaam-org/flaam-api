from django.urls import path

from .views import FavouriteTagView, TagDetailView, TagListView

urlpatterns = [
    path("tags", TagListView.as_view()),
    path("tag/<str:name>", TagDetailView.as_view()),
    path("tag/<str:name>/favourite", FavouriteTagView.as_view()),
]
