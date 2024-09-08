

from SqlDynamicCalculator.Models.JoinedTableListModel import *


@dataclass
class JoinMainTableModel:
	main_table_name: str = None
	joined_table_name_right: str = None
	left_join_index: str = None
	right_join_index: str = None
	how_to_join: str = "left"
	joined_table_list: list[JoinedTableListModel] = field(default_factory=list)

	def _create_join_table_string(self):
		query = []
		for table in self.joined_table_list:
			q = f"""
            {table.how_to_join} {table.joined_table_name_right}\n
            ON {table.joined_table_name_left}.'{table.left_join_index}'={table.joined_table_name_right}.'{table.right_join_index}'
            """
			query.append(q)
		res = "".join(query)
		return res

	def get_joined_table(self) -> str:
		join_table_query = f"""
            FROM {self.main_table_name}
            {self._create_join_table_string()}
            """
		return join_table_query
