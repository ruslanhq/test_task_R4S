from django.urls import path

from apps.robots.views import create_robot

urlpatterns = [
    path("create", create_robot, name="create_robot"),
]
