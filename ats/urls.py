from django.contrib import admin
from django.urls import include, path

from ats import settings


urlpatterns = [
    path("candidates/", include("candidates.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
