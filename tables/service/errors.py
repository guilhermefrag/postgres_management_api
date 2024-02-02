from django.forms import ValidationError

from generics.classes.database_manager import DatabaseManager


def table_error_handling(table_name, schema_name, database_name="default"):
    if table_name is None or not table_name:
        raise ("Table name is required.")
    if table_name.startswith("pg_"):
        raise ValidationError("Table name cannot start with 'pg_'")
    if check_existent_table(table_name, database_name):
        raise ValidationError("Table already exists.")
    
def check_existent_table(table_name: str, database_name) -> bool:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = '{table_name}'
            )"""
        )
        return db.fetchone()[0]