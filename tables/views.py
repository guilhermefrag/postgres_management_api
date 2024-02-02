from typing import List

from django.http import HttpResponse
from django.forms import ValidationError
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tables.repositories.tables import (
    create_table_repository,
    get_all_tables_repository,
    get_table_from_schema_repository,
    get_tables_from_schema_repository,
    get_table_repository,
    update_table_repository,
)
from tables.service.errors import table_error_handling
from utils.types.table import Table

# Create your views here.


@api_view(["GET"])
def get_all_tables(request: HttpRequest) -> List[Table]:
    """
    Get all tables
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        tables = get_all_tables_repository(database_name)
        if not tables:
            return Response(
                {"error": "Tables not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"tables": tables}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_table(request: HttpRequest, table_name: str) -> Table:
    """
    Get a table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        table = get_table_repository(table_name, database_name)
        if not table:
            return Response(
                {"error": "Table not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"table": table}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_tables_from_schema(request: HttpRequest, schema_name: str) -> List[Table]:
    """
    Get a table from a schema
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        tables = get_tables_from_schema_repository(schema_name, database_name)
        if not tables:
            return Response(
                {"error": "Tables not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"tables": tables}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_table_from_schema(
    request: HttpRequest, schema_name: str, table_name: str
) -> Table:
    """
    Get a table from a schema
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        table = get_table_from_schema_repository(table_name, schema_name, database_name)
        if not table:
            return Response(
                {"error": "Table not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"table": table}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_table(request: HttpRequest) -> HttpResponse:
    """
    Create a new table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        table_name = request.data.get("table_name")
        schema_name = request.data.get("schema_name")
        table_error_handling(table_name, schema_name, database_name)
        create_table_repository(table_name, schema_name, database_name)
        return Response(
            {
                "message": f"Table {table_name} created successfully in schema {schema_name} !"
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as error:
        return Response(
            {"error": error.message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
def update_table(request: HttpRequest, table_name: str) -> HttpResponse:
    """
    Update a table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        new_table_name = request.data.get("new_table_name")
        schema_name = request.data.get("schema_name")
        table_error_handling(new_table_name, schema_name, database_name)
        with transaction.atomic():
            update_table_repository(
                table_name, new_table_name, schema_name, database_name
            )
        return Response(
            {
                "message": f"Table {table_name} updated to {new_table_name} successfully in schema {schema_name} !"
            },
            status=status.HTTP_200_OK,
        )
    except Exception as error:
        return Response(
            {"error": error.message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
