
from django.forms import ValidationError
from generics.classes.database_manager import DatabaseManager

def schema_error_handling(schema_name):
    if schema_name is None or not schema_name:
        raise ("Schema name is required.")
    if schema_name.startswith("pg_"):
        raise ValidationError("Schema name cannot start with 'pg_'")
    if schema_name == "information_schema":
        raise ValidationError("Schema name cannot be 'information_schema'")
    if check_existent_schema(schema_name):
        raise ValidationError("Schema already exists.")

def check_existent_schema(schema_name: str) -> bool:
    with DatabaseManager("default") as db:
        db.execute(
            f"""SELECT EXISTS (
                SELECT 1
                FROM information_schema.schemata
                WHERE schema_name = '{schema_name}'
            )"""
        )
        return db.fetchone()[0]