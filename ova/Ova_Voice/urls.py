from django.urls import path

from . import views
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path("", views.index, name="index"),
]


if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
from django.urls import include

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + debug_toolbar_urls()