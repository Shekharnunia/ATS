from django.urls import path

from . import views

urlpatterns = [
    path("", views.CandidateListCreateView.as_view(), name="candidate-list-create"),
    path(
        "<int:pk>/",
        views.CandidateRetrieveUpdateDestroyView.as_view(),
        name="candidate-retrieve-update-destroy",
    ),
    path("search/", views.CandidateSearchAPIView.as_view(), name="candidate-search"),
]
