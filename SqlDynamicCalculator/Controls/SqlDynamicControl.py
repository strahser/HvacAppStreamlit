from SqlDynamicCalculator.Controls.TabsViewControl import *
from dataclasses import dataclass


class SqlDynamicControl:
	def __init__(self, tabs_view: TabsViewControl):
		self.tabs_view = tabs_view

	def __check_custom_functions(self):
		if self.tabs_view.custom_function:
			return f",{self.tabs_view.custom_function}\n"
		else:
			return ""

	def create_sql_query(self):
		sql = f"""
		        SELECT\n{self.tabs_view.joined_table_control.selected_columns_parsing_to_string}{self.__check_custom_functions()}
		        {self.tabs_view.joined_table_tables_string}\n{self.tabs_view.where_filter}
		        """
		return sql
