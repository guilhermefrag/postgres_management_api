from django.urls import path

from schemas.views import create_schema

urlpatterns = [
    path("", create_schema, name="create_schema"),
]
