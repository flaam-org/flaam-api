from django.urls import path

from .views import TagDetailView

urlpatterns = [
    path("tag/<str:name>", TagDetailView.as_view()),
]
