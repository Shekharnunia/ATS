from django.urls import include, path


urlpatterns = [
    path("v1/", include("candidates.api.v1.urls")),
    path("v2/", include("candidates.api.v2.urls")),
]
