from django.urls import path

from schemas.views import create_schema, get_schemas, get_schema,update_schema

urlpatterns = [
    path("", create_schema, name="create_schema"),
    path("getall/", get_schemas, name="get_schemas"),
    path("<str:schema_name>/", get_schema, name="get_schema"),
    path("<str:schema_name>/update/", update_schema, name="update_schema"),
]
