from typing import TypedDict, Optional

class Table(TypedDict):
    table_catalog: str
    table_schema: str
    table_name: str
    table_type: str
    self_referencing_column_name: Optional[str]
    reference_generation: Optional[str]
    user_defined_type_catalog: Optional[str]
    user_defined_type_schema: Optional[str]
    user_defined_type_name: Optional[str]
    is_insertable_into: str
    is_typed: str
    commit_action: Optional[str]