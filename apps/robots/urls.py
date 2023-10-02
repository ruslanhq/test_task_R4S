from django.urls import path

from apps.robots.views import create_robot, download_excel_summary

urlpatterns = [
    path("create", create_robot, name="create_robot"),
    path("download_file", download_excel_summary, name="download_excel_file")
]
