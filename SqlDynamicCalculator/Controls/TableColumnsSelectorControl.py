from Upload.UploadLayout import UploadLayout
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputViewControl import InputViewControl
import streamlit as st
import pandas as pd
from StaticData.AppConfig import MenuChapters


class TableColumnsSelectorControl:

	def __init__(self, upload_layout: UploadLayout, conn=SqlConnector.conn_sql, key=""):
		"""SELECT table FROM sqlite_master.Get Columns Filter. return columns string join"""
		self.conn = conn
		self.key = key
		self.upload_layout = upload_layout
		self.filter_columns = None
		self.table_filter = None

	def get_columns_for_query(self, table_name: str = ""):

		st.markdown(f"#### Select Columns Table {self.key} {table_name} ")
		# dynamic view
		with st.expander("Input Space Data"):
			table = self.__is_table_from_selected_checkbox_exist(table_name)
			if not table.empty:
				self.filter_columns = st.multiselect("Select Columns",
				                                     table.columns,
				                                     default=table.columns.to_list(),
				                                     key=f"{self.key} {MenuChapters.analytics} table_filter")
				_filter_columns_string = [f"{self.selected_sheet}.'{val}'" for val in self.filter_columns]
				_joined_column_strings = ", ".join(_filter_columns_string)
				sql = f""" SELECT {_joined_column_strings} FROM {self.selected_sheet} """
				try:
					st.expander("Table Data").write(pd.read_sql(sql, self.conn))
				except Exception as e:
					st.warning(e)
				return _joined_column_strings

	def __is_table_from_selected_checkbox_exist(self, table_name=""):

		if table_name:
			try:
				sql = f""" SELECT * FROM {table_name} """
				self.selected_sheet = table_name
				table =pd.read_sql(sql, self.conn)
				return table
			except:
				return None

		else:
			return self._load_db_table_or_db_view_sheet()

	def _load_db_table_or_db_view_sheet(self,
	                                    index_book: int = 0,
	                                    index_sheet: int = 0):
		input_view_control = InputViewControl(self.upload_layout, f'{self.key} {MenuChapters.analytics}')
		table = input_view_control.create_input_view()
		st.write(table)
		self.selected_sheet = input_view_control.input_view.selected_excel_sheet
		st.write(self.selected_sheet)
		return table
