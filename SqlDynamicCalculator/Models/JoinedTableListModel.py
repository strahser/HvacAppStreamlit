from dataclasses import dataclass, field


@dataclass
class JoinedTableListModel:
	joined_table_name_left: str = None
	joined_table_name_right: str = None
	left_join_index: str = None
	right_join_index: str = None
	how_to_join: str = "LEFT JOIN"
