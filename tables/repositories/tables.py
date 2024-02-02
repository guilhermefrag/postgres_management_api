from generics.classes.database_manager import DatabaseManager


def get_all_tables_repository(database_name: str = "default") -> dict:
    with DatabaseManager(database_name) as db:
        json_data = []
        db.execute(
            """SELECT row_to_json(tables) 
                FROM (SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema NOT LIKE 'pg_%' 
                    AND table_schema != 'information_schema') tables"""
        )
        json_data.extend(item[0] for item in db.fetchall())

        return json_data


def get_table_repository(table_name: str, database_name: str = "default") -> dict:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT row_to_json(tables) 
                FROM (SELECT * 
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}') tables"""
        )

        return db.fetchone()


def get_tables_from_schema_repository(
    schema_name: str, database_name: str = "default"
) -> dict:
    with DatabaseManager(database_name) as db:
        json_data = []
        db.execute(
            f"""SELECT row_to_json(tables) 
                FROM (SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema = '{schema_name}') tables"""
        )
        json_data.extend(item[0] for item in db.fetchall())

        return json_data


def get_table_from_schema_repository(
    table_name: str, schema_name: str, database_name: str = "default"
) -> dict:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT row_to_json(tables) 
                FROM (SELECT * 
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}') tables"""
        )

        return db.fetchone()


def create_table_repository(
    table_name: str, schema_name: str, database_name: str = "default"
) -> None:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""CREATE TABLE {schema_name}.{table_name} (
                id SERIAL PRIMARY KEY
            )"""
        )

        return
    
def update_table_repository(
    table_name: str, new_table_name: str, schema_name: str, database_name: str = "default"
) -> None:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""ALTER TABLE {schema_name}.{table_name} RENAME TO {new_table_name}"""
        )

        return
