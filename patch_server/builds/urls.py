from django.urls import path
from .views import get_new_files, newer_version_availible

urlpatterns = [
    path("compare/", get_new_files),
    path("ewer_version_availible/", newer_version_availible),
]
