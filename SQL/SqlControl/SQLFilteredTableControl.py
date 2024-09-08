from SQL.SqlModel.SqlQueryModel import SqlQueryModel
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd


class SQLFilteredTableControl:
	def __init__(self):
		"""add id selected values to db"""
		self.sql_filtered_list = SqlQueryModel("filtered_table", SqlConnector.conn_sql)
		self.sql_filtered_list.create_table()
		self.clicked_filter_id_list = self.sql_filtered_list.df_read_sql()["filtered_id_column"].to_list()
	
	def insert_selected_id_from_df_to_sql_db(self, selected_id: pd.DataFrame, id_column_name: str = 'filtered_id_column'):
		"""from plotly_events get_selected_id """
		self.sql_filtered_list.insert_value(selected_id[id_column_name].values[0])
	
	def insert_selected_id_to_sql_db(self, id_column_name: str, selected_id: str = "Null"):
		"""from plotly_events get_selected_id """
		selected_id = selected_id if selected_id else "Null"
		self.sql_filtered_list.insert_value(id_column_name, selected_id, )
	
	def drop_table(self):
		self.sql_filtered_list.drop_table()
