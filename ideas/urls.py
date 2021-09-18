from django.urls import path

from .views import IdeaListView, IdeaDetailView

urlpatterns = [
    path("ideas", IdeaListView.as_view(), name="ideas"),
    path("idea/<int:pk>", IdeaDetailView.as_view(), name="idea"),
]
