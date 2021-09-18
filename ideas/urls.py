from django.urls import path

from .views import IdeaDetailView, IdeaListView

urlpatterns = [
    path("ideas", IdeaListView.as_view(), name="ideas"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea"),
]
