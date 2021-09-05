from django.urls import path

from .views import TagDetailView, TagListView

urlpatterns = [
    path("tags", TagListView.as_view()),
    path("tag/<str:name>", TagDetailView.as_view()),
]
