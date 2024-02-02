from typing import TypedDict, Optional

class Schema(TypedDict):
    catalog_name: str
    schema_name: str
    schema_owner: str
    default_character_set_catalog: Optional[str]
    default_character_set_schema: Optional[str]
    default_character_set_name: Optional[str]
    sql_path: Optional[str]
