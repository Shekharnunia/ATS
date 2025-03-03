from django.urls import include, path

from .api.v1 import views

urlpatterns = [
    path("v1/", include("candidates.api.v1.urls")),
    path("v2/", include("candidates.api.v2.urls")),
]
