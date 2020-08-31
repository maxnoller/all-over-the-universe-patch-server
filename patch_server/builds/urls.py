from django.urls import path
from .views import get_new_files, newer_version_availible

urlpatterns = [
    path("compare/", get_new_files),
    path("check_newest_version/", newer_version_availible),
]