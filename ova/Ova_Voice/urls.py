from django.urls import path

from . import views
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path("", views.index, name="index"),
]
from .views import ToggleOVAView

urlpatterns = [
    path('toggle-ova/', ToggleOVAView.as_view(), name='toggle-ova'),
]


if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
from django.urls import include

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + debug_toolbar_urls()