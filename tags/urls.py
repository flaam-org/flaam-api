from django.urls import path

from .views import FavouriteTagView, TagDetailView, TagListView

urlpatterns = [
    path("tags", TagListView.as_view()),
    path("tag/<int:pk>", TagDetailView.as_view()),
    path("tag/<int:pk>/favourite", FavouriteTagView.as_view()),
]
