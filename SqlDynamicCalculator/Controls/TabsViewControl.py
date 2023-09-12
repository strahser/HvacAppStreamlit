import sqlite3

from streamlit_ace import st_ace

from SqlDynamicCalculator.Controls.JoinedTableControl import JoinedTableControl
from Upload.UploadLayout import UploadLayout
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputView import *


class TabsViewControl:
	
	def __init__(self, upload_layout: UploadLayout, conn: sqlite3.Connection = SqlConnector.conn_sql):
		self.where_filter = None
		self.custom_function = None
		self.joined_table_tables_string = None
		self.joined_table_control = None
		self.upload_layout = upload_layout
		self.conn = conn
	
	def show_tabs_view(self) -> None:
		input_table_tab, option_tab, custom_function_tab = st.tabs(["Input Table", "Option", "Custom Function"])
		with input_table_tab:
			with st.expander("Show Input Table"):
				try:
					self.joined_table_control = JoinedTableControl(self.upload_layout, self.conn)
					self.joined_table_control.create_join_table_columns()
				except:
					return None
		with option_tab:
			with st.expander("Show Options"):
				self.joined_table_tables_string = self.joined_table_control \
					.populate_model_and_index_join_view() \
					.get_joined_table()
		with custom_function_tab:
			st.write("SQL Function")
			self.custom_function = st_ace(placeholder="Function (group by function) ",language="sql",key="ace custom_function")
			st.write("SQL Filter")
			self.where_filter = st_ace(placeholder="Filter (group by column) ",language="sql",key="ace where_filter")
