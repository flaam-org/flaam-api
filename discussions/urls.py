from django.urls import path

from .views import (
    DiscussionCommentDetailView,
    DiscussionCommentListView,
    DiscussionDetailView,
    DiscussionListView,
    VoteDiscussionView,
)

urlpatterns = [
    path(
        "discussions",
        DiscussionListView.as_view(),
        name="discussion-list",
    ),
    path(
        "discussion/<int:pk>",
        DiscussionDetailView.as_view(),
        name="discussion-detail",
    ),
    path(
        "discussion/<int:pk>/vote",
        VoteDiscussionView.as_view(),
        name="vote-discussion",
    ),
    path(
        "discussion/comments",
        DiscussionCommentListView.as_view(),
        name="discussion-comment-list",
    ),
    path(
        "discussion/comment/<int:pk>",
        DiscussionCommentDetailView.as_view(),
        name="discussion-comment-detail",
    ),
]
