from django.urls import path

from .views import BookmarkIdeaView, IdeaDetailView, IdeaListView

urlpatterns = [
    path("ideas", IdeaListView.as_view(), name="ideas"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea"),
    path("idea/<int:pk>/bookmark", BookmarkIdeaView.as_view(), name="idea"),
]
