from generics.classes.database_manager import DatabaseManager


def create_schema_repository(schema_name: str) -> None:
    with DatabaseManager("default") as db:
        db.execute(f"CREATE SCHEMA {schema_name}")
    print(f"Schema {schema_name} created.")