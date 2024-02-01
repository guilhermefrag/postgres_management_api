from typing import TypedDict

class Schema(TypedDict):
    catalog_name: str
    schema_name: str
    schema_owner: str
    default_character_set_catalog: str
    default_character_set_schema: str
    default_character_set_name: str
    sql_path: str
