from generics.classes.database_manager import DatabaseManager
from schemas.service.errors import schema_error_handling


def get_all_schemas_repository(database_name: str = "default") -> dict:
    with DatabaseManager(database_name) as db:
        json_data = []
        db.execute(
            """SELECT row_to_json(schemas) 
                FROM (SELECT * 
                    FROM information_schema.schemata
                    WHERE schema_name NOT LIKE 'pg_%' 
                    AND schema_name != 'information_schema') schemas"""
        )
        json_data.extend(item[0] for item in db.fetchall())

        return json_data


def get_schema_repository(schema_name: str, database_name: str = "default") -> dict:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT row_to_json(schemas) 
                FROM (SELECT * 
                    FROM information_schema.schemata
                    WHERE schema_name = '{schema_name}') schemas"""
        )

        return db.fetchone()


def create_schema_repository(schema_name: str, database_name: str = "default") -> None:
    schema_error_handling(schema_name)
    with DatabaseManager(database_name) as db:
        db.execute(f"CREATE SCHEMA {schema_name}")


def update_schema_repository(schema_name: str, new_schema_name: str, database_name: str = "default") -> None:
    schema_error_handling(new_schema_name)
    with DatabaseManager(database_name) as db:
        db.execute(f"ALTER SCHEMA {schema_name} RENAME TO {new_schema_name}")
