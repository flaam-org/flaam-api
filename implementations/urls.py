from django.urls import path

from .views import (
    AcceptImplementationView,
    ImplementationCommentDetailView,
    ImplementationCommentListView,
    ImplementationDetailView,
    ImplementationListView,
    ValidateImplementationView,
    VoteImplementationView,
)

urlpatterns = [
    path(
        "implementations",
        ImplementationListView.as_view(),
        name="implementation-list",
    ),
    path(
        "implementation/<int:pk>",
        ImplementationDetailView.as_view(),
        name="implementation-detail",
    ),
    path(
        "implementation/<int:pk>/vote",
        VoteImplementationView.as_view(),
        name="vote-implementation",
    ),
    path(
        "implementation/<int:pk>/accept",
        AcceptImplementationView.as_view(),
        name="accept-implementation",
    ),
    path(
        "implementation/<int:pk>/validate",
        ValidateImplementationView.as_view(),
        name="validate-implementation",
    ),
    path(
        "implementation/comments",
        ImplementationCommentListView.as_view(),
        name="implementation-comment-list",
    ),
    path(
        "implementation/comment/<int:pk>",
        ImplementationCommentDetailView.as_view(),
        name="implementation-comment-detail",
    ),
]
