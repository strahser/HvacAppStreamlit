import pandas as pd
from SQL.SqlView.AggTabelView import AggTabelView
from SQL.SqlControl.SqlTableToolsControl import SqlTableToolsControl


class SqlDataSelectAndUpdateControl:
	def __init__(self, input_df: pd.DataFrame, table_name: str):
		self.input_df = input_df
		self.table_name = table_name

	def create_agg_table(self):
		agg_table = AggTabelView(self.input_df)
		selected_table_value = agg_table.create_filtered_table()
		return selected_table_value

	def create_sql_table_tools(self, selected_table_value):
		sql_table_tools = SqlTableToolsControl(self.input_df, selected_table_value, self.table_name)
		sql_table_tools.create_crud_operation()