from django.urls import path
from .views import get_new_files, newer_version_availible, get_newest_version

urlpatterns = [
    path("compare/", get_new_files),
    path("newer_version_availible/", newer_version_availible),
    path("get_newest_version/", get_newest_version),
]
