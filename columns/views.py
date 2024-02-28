from typing import List

from django.http import HttpResponse
from django.forms import ValidationError
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from columns.repositories.column import create_column_repository, get_all_columns_repository, get_column_repository, get_columns_from_table_repository
from utils.types.columns import Column


# Create your views here.
@api_view(["GET"])
def get_all_columns(request: HttpRequest, table_name: str, schema_name: str) -> List[Column]:
    """
    Get all columns
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        columns = get_all_columns_repository(table_name, schema_name, database_name)
        if not columns:
            return Response(
                {"error": "Columns not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"columns": columns}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_column(request: HttpRequest, table_name: str, schema_name: str, column_name: str) -> Column:
    """
    Get a column
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        column = get_column_repository(table_name, schema_name, column_name, database_name)
        if not column:
            return Response(
                {"error": "Column not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"column": column}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_columns_from_table(request: HttpRequest, table_name: str, schema_name: str) -> List[Column]:
    """
    Get all columns from a table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        columns = get_columns_from_table_repository(table_name, schema_name, database_name)
        if not columns:
            return Response(
                {"error": "Columns not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"columns": columns}, status=status.HTTP_200_OK)

@extend_schema(
    request={
        "examples": {
            "example": {"schema_name": "example_schema", "table_name": "example_table", "column_name": "example_column"}
        }
    },
    responses={201: {"description": "Column created successfully"}},
)
@api_view(["POST"])
def create_column(request: HttpRequest) -> HttpResponse:
    """
    Create a new table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        table_name = request.data.get("table_name")
        schema_name = request.data.get("schema_name")
        column_name = request.data.get("column_name")
        column_type = request.data.get("column_type")
        create_column_repository(table_name, schema_name, column_name, column_type, database_name)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )