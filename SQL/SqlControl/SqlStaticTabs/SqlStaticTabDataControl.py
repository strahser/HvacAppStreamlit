import streamlit as st
import pandas as pd
from SQL.SqlControl.SqlStaticTabs.SheetsTabView import SheetsTabView
from InputView.InputViewControl import InputViewControl
from StaticData.AppConfig import MenuChapters, StaticVariable
from SQL.SqlModel.SqlConnector import SqlConnector
from Upload import UploadLayout
from Session.StatementConfig import StatementConstants


class SelectSheetAndBookNames:
	def __init__(self, upload_layout: UploadLayout, key: str):
		self.upload_layout = upload_layout
		self.key = key
		self.input_view_control = InputViewControl(self.upload_layout, self.key, connector=SqlConnector.conn_sql)
		self.input_view_control.create_input_view()
		self.table_name = self.input_view_control.sheet_name
		self.selected_sheet = self.input_view_control.input_view.selected_excel_sheet

	@property
	def excel_books_data(self):
		if self.input_view_control.input_view.selected_excel_books in st.session_state[
			StatementConstants.table_db].keys():
			return st.session_state[StatementConstants.table_db][
				self.input_view_control.input_view.selected_excel_books]
		if (
				self.input_view_control.input_view.selected_excel_books in
				st.session_state[StatementConstants.category_dictionary].keys()
		):
			return st.session_state[StatementConstants.category_dictionary][self.input_view_control.input_view.selected_excel_books]

	def _select_sheet_or_book(self) -> str:
		if hasattr(self.input_view_control.input_view, "selected_excel_books"):
			"при выборе вид вылетает из за отсутвия аттрибута selected_excel_books"
			if self.input_view_control.input_view.selected_excel_books != StatementConstants.all_tables_db:
				"если не сделать проверку будет слишком много табов сгенерено"
				return self.excel_books_data
			else:
				return self.selected_sheet
		else:
			"возвращаем выбранный вид"
			self.excel_books_data = self.table_name
			return self.excel_books_data

	@excel_books_data.setter
	def excel_books_data(self, value):
		self._excel_books_data = value


class SqlStaticTabDataControl:
	def __init__(self, upload_layout: UploadLayout, connector=SqlConnector.conn_sql):
		self.connector = connector
		self.upload_layout = upload_layout
		self.tables_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		self.views_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		self.category_name = st.session_state[StatementConstants.category_dictionary]
		self.key = MenuChapters.analytics

	def create_sample_tables_db(self):
		with st.expander("All Tables and Views"):
			col1, col2,col3 = st.columns(3)
			with col1:
				st.markdown("#### All Tables Names #####")
				st.dataframe(pd.DataFrame({"Table Names": self.tables_name}))
			with col2:
				st.markdown("#### All Views Names #####")
				st.dataframe(pd.DataFrame({"View Names": self.views_name}))
			with col3:
				st.markdown("#### All Category Names #####")
				st.write(self.category_name)
		with st.expander("Selected Table"):
			selected_sheet_and_books = SelectSheetAndBookNames(self.upload_layout, self.key)
			tab_view = SheetsTabView(selected_sheet_and_books.excel_books_data, self.connector, self.key)
			tab_view.choose_table_or_view_data()
			self._create_unique_column_data(selected_sheet_and_books.selected_sheet)

	def _create_unique_column_data(self, selected_sheet):
		with st.expander("Select unique column data"):
			col = st.columns(3)
			try:
				df = pd.read_sql_query(f"select * from {selected_sheet}", con=self.connector)
				selected_column = st.multiselect("select column for checking", df.columns)
				df_list = []
				for data in selected_column:
					unique_column_data = pd.DataFrame({data: df[data].unique()})
					df_list.append(unique_column_data)
				st.write(pd.concat(df_list, axis=1))
			except Exception as e:
				st.warning(e)
