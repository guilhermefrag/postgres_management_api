from typing import List

from django.http import HttpResponse
from django.forms import ValidationError
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema


# Create your views here.
@extend_schema(
    request={
        "examples": {
            "example": {"schema_name": "example_schema", "table_name": "example_table", "column_name": "example_column"}
        }
    },
    responses={201: {"description": "Column created successfully"}},
)
@api_view(["POST"])
def create_table(request: HttpRequest) -> HttpResponse:
    """
    Create a new table
    """
    try:
        database_name = request.headers.get("Db-Name", "default")
        table_name = request.data.get("table_name")
        schema_name = request.data.get("schema_name")
        column_name = request.data.get("column_name")
        column_type = request.data.get("column_type")
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )