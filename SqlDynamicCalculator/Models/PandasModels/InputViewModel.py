from SQL.SqlModel import SqlConnector
from library_hvac_app.list_custom_functions import flatten
import pandas as pd


class InputViewModel:
	def __init__(self, excel_sheet: str, conn=SqlConnector.conn_sql):
		self.sql_views = None
		self.loaded_df = None
		self.loaded_sheet = None
		self.conn = conn
		self.excel_sheet = excel_sheet

	def get_loaded_loaded_sheet(self):
		self.loaded_sheet = flatten(self.conn.cursor() \
		                            .viewer_execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
		if self.excel_sheet in self.loaded_sheet:
			self.loaded_df = pd.read_sql(f"select * from {self.excel_sheet}", self.conn)
			return self.loaded_df

	def get_sql_views(self, selected_view):
		self.sql_views = self.conn.cursor().viewer_execute("SELECT name FROM sqlite_master WHERE type='view';").fetchall()
		if selected_view in flatten(self.sql_views):
			loaded_view = pd.read_sql(f"select * from {selected_view}", self.conn)
			return loaded_view
