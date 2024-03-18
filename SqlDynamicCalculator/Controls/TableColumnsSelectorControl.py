from Upload.UploadLayout import UploadLayout
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputViewControl import InputViewControl
import streamlit as st
import pandas as pd
from StaticData.AppConfig import MenuChapters


class TableColumnsSelectorControl:

	def __init__(self, conn=SqlConnector.conn_sql, key=""):
		"""SELECT table FROM sqlite_master.Get Columns Filter. return columns string join"""
		self.conn = conn
		self.key = key
		self.table_filter = None

	def get_columns_for_query(self, table_name: str = ""):

		st.markdown(f"#### Select Columns Table {self.key} {table_name} ")
		# dynamic view
		with st.expander("Input Space Data"):
			table = self.__is_table_from_selected_checkbox_exist(table_name)
			if not table.empty:
				filter_columns = st.multiselect("Select Columns",
				                                     table.columns,
				                                     default=table.columns.to_list(),
				                                     key=f"{self.key} {MenuChapters.analytics} table_filter")
				alias = st.text_input("Choose table alias",value=table_name[0])
				_filter_columns_string = [f"{alias}.'{val}'" for val in filter_columns]
				_joined_column_strings = ", ".join(_filter_columns_string)
				sql = f""" SELECT {_joined_column_strings}\n FROM {table_name} AS {alias}"""
				try:
					st.expander("Table Data").write(pd.read_sql(sql, self.conn))
				except Exception as e:
					st.warning(e)
				return sql

	def __is_table_from_selected_checkbox_exist(self, table_name=""):
		if table_name:
			try:
				sql = f""" SELECT * FROM {table_name} """
				table = pd.read_sql(sql, self.conn)
				return table
			except:
				return None

	def _load_db_table_or_db_view_sheet(self, upload_layout):
		input_view_control = InputViewControl(upload_layout, f'{self.key} {MenuChapters.analytics}')
		table = input_view_control.create_input_view()
		st.write(table)
		self.selected_sheet = input_view_control.input_view.selected_excel_sheet
		st.write(self.selected_sheet)
		return table
