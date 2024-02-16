from typing import List
from generics.classes.database_manager import DatabaseManager
from utils.types.columns import Column

def get_all_columns_repository(table_name: str, schema_name: str, database_name: str = "default") -> List[Column]:
    with DatabaseManager(database_name) as db:
        json_data = []
        db.execute(
            f"""SELECT row_to_json(columns) 
                FROM (SELECT * 
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}') columns"""
        )
        json_data.extend(item[0] for item in db.fetchall())

        return json_data
    
def get_column_repository(table_name: str, schema_name: str, column_name: str, database_name: str = "default") -> Column:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT row_to_json(columns) 
                FROM (SELECT * 
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}'
                    AND column_name = '{column_name}') columns"""
        )

        return db.fetchone()
    
def get_columns_from_table_repository(table_name: str, schema_name: str, database_name: str = "default") -> List[Column]:
    with DatabaseManager(database_name) as db:
        json_data = []
        db.execute(
            f"""SELECT row_to_json(columns) 
                FROM (SELECT * 
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}') columns"""
        )
        json_data.extend(item[0] for item in db.fetchall())

        return json_data
    
def get_column_from_table_repository(table_name: str, schema_name: str, column_name: str, database_name: str = "default") -> Column:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""SELECT row_to_json(columns) 
                FROM (SELECT * 
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}'
                    AND column_name = '{column_name}') columns"""
        )

        return db.fetchone()

def create_column_repository(
    table_name: str, schema_name: str, column_name: str, column_type: str, database_name: str = "default"
) -> None:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""ALTER TABLE {schema_name}.{table_name} 
                ADD COLUMN {column_name} {column_type}"""
        )

        return
    
def update_column_repository(
    table_name: str, schema_name: str, column_name: str, new_column_name: str, new_column_type: str, database_name: str = "default"
) -> None:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""ALTER TABLE {schema_name}.{table_name} 
                RENAME COLUMN {column_name} TO {new_column_name}"""
        )
        db.execute(
            f"""ALTER TABLE {schema_name}.{table_name} 
                ALTER COLUMN {new_column_name} TYPE {new_column_type}"""
        )

        return
    
def delete_column_repository(
    table_name: str, schema_name: str, column_name: str, database_name: str = "default"
) -> None:
    with DatabaseManager(database_name) as db:
        db.execute(
            f"""ALTER TABLE {schema_name}.{table_name} 
                DROP COLUMN {column_name}"""
        )

        return