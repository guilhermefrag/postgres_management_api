from typing import List

from django.http import HttpResponse
from django.forms import ValidationError
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from utils.types.schema import Schema

from .repositories.schemas import (
    create_schema_repository,
    delete_schema_repository,
    get_all_schemas_repository,
    get_schema_repository,
    update_schema_repository,
)

from drf_spectacular.utils import extend_schema

@api_view(["GET"])
@transaction.atomic
def get_schemas(request: HttpRequest) -> List[Schema]:
    """
    Get all schemas
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        schemas = get_all_schemas_repository(database_name)
        if not schemas:
            return Response(
                {"error": "Schemas not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"schemas": schemas}, status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def get_schema(request: HttpRequest, schema_name: int) -> Schema:
    """
    Get a schema by its name.
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        schema = get_schema_repository(schema_name, database_name)
        if not schema:
            return Response(
                {"error": "Schema not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"schema": schema}, status=status.HTTP_200_OK)

@extend_schema(
    request={"examples": {"example": {"schema_name": "example_schema"}}},
    responses={201: {"description": "Schema created successfully"}},
)
@api_view(["POST"])
@transaction.atomic
def create_schema(request: HttpRequest) -> HttpResponse:
    """
    Create a new schema.
    """
    database_name = request.headers.get("Db-Name", "default")
    schema_name = request.data.get("schema_name")
    if not schema_name:
        return Response(
            {"error": "Schema name is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        create_schema_repository(schema_name, database_name)
    except ValidationError as e:
        return Response(
            {"error": e.message},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"message": f"Schema {schema_name} created!"}, status=status.HTTP_201_CREATED
    )

@extend_schema(
    request={"examples": {"example": {"new_schema_name": "new_example_schema"}}},
    responses={201: {"description": "Schema updated successfully"}},
)
@api_view(["PUT"])
@transaction.atomic
def update_schema(request: HttpRequest, schema_name: int) -> HttpResponse:
    """
    Update a schema by its name.
    """
    database_name = request.headers.get("Db-Name", "default")
    new_schema_name = request.data.get("new_schema_name")
    if not new_schema_name:
        return Response(
            {"error": "New schema name is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        update_schema_repository(schema_name, new_schema_name, database_name)
    except ValidationError as e:
        return Response(
            {"error": e.message},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"message": f"Schema {schema_name} updated to {new_schema_name}!"},
        status=status.HTTP_200_OK,
    )
    
@api_view(["DELETE"])
def delete_schema(request: HttpRequest, schema_name: int) -> HttpResponse:
    """
    Delete a schema by its name.
    """
    database_name = request.headers.get("Db-Name", "default")
    try:
        delete_schema_repository(schema_name, database_name)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"message": f"Schema {schema_name} deleted!"}, status=status.HTTP_200_OK
    )
