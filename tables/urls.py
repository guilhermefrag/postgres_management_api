from django.urls import path

from tables.views import (
    get_all_tables,
    get_table,
    get_tables_from_schema,
    get_table_from_schema,
    create_table,
    update_table,
    delete_table,
)


urlpatterns = [
    path("", create_table, name="create table"),
    path("getall/", get_all_tables, name="get_all_tables"),
    path("<str:table_name>/update/", update_table, name="update table"),
    path("<str:table_name>/", get_table, name="get_table"),
    path(
        "schema/<str:schema_name>/",
        get_tables_from_schema,
        name="get tables from schema",
    ),
    path(
        "<str:schema_name>/<str:table_name>/",
        get_table_from_schema,
        name="get table from schema",
    ),
    path("<str:table_name>/delete/", delete_table, name="delete table"),
]
