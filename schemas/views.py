from django.http import HttpResponse
from django.forms import ValidationError
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .repositories.schemas import (
    create_schema_repository,
    get_all_schemas_repository,
    get_schema_repository,
)


@api_view(["GET"])
@transaction.atomic
def get_schemas(request: HttpRequest) -> HttpResponse:
    """
    Get all schemas
    """
    try:
        schemas = get_all_schemas_repository()
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"schemas": schemas}, status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def get_schema(request: HttpRequest, schema_name: int) -> HttpResponse:
    """
    Get a schema by its name.
    """
    try:
        schema = get_schema_repository(schema_name)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"schema": schema}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def create_schema(request: HttpRequest) -> HttpResponse:
    """
    Create a new schema.
    """
    schema_name = request.data.get("schema_name")
    if not schema_name:
        return Response(
            {"error": "Schema name is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        create_schema_repository(schema_name)
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
