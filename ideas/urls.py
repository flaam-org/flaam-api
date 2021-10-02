from django.urls import path

from .views import BookmarkIdeaView, IdeaDetailView, IdeaListView, VoteIdeaView

urlpatterns = [
    path("ideas", IdeaListView.as_view(), name="ideas"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea"),
    path("idea/<int:pk>/vote", VoteIdeaView.as_view(), name="idea_vote"),
    path("idea/<int:pk>/bookmark", BookmarkIdeaView.as_view(), name="idea_bookmark"),
]
