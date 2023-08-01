import streamlit as st
import pandas as pd
from SQL.SqlControl.SqlStaticTabs.SheetsTabView import SheetsTabView
from InputView.InputViewControl import InputViewControl
from StaticData.AppConfig import MenuChapters, StaticVariable
from SQL.SqlModel.SqlConnector import SqlConnector
from Upload import UploadLayout
from Session.StatementConfig import StatementConstants


class SqlStaticTabDataControl:
	def __init__(self, upload_layout: UploadLayout, connector=SqlConnector.conn_sql):
		self.connector = connector
		self.upload_layout = upload_layout
		self.tables_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		self.views_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		self.key = MenuChapters.analytics

	def create_sample_tables_db(self):
		with st.expander("All Tables and Views"):
			col1, col2 = st.columns(2)
			with col1:
				st.markdown("#### All Tables Names #####")
				st.dataframe(pd.DataFrame({"Table Names": self.tables_name}))
			with col2:
				st.markdown("#### All Views Names #####")
				st.dataframe(pd.DataFrame({"View Names": self.views_name}))
		with st.expander("Selected Table"):
			selected_sheet = self._select_sheet_or_book()
			print(selected_sheet)
			self._create_unique_column_data(selected_sheet)
			tab_view = SheetsTabView(selected_sheet, self.connector, self.key)
			tab_view.choose_table_or_view_data()
	def _create_unique_column_data(self,selected_sheet):
		try:
			df =  pd.read_sql_query(f"select * from {selected_sheet}",con=self.connector)
			selected_column =st.selectbox("select column for checking", df.columns)
			unique_column_data = df[selected_column].unique()
			return unique_column_data
		except Exception as e:
			st.warning(e)

	def _select_sheet_or_book(self) -> str:
		input_view_control = InputViewControl(self.upload_layout, self.key, connector=SqlConnector.conn_sql)
		input_view_control.create_input_view()
		table_name = input_view_control.sheet_name
		if hasattr(input_view_control.input_view, "selected_excel_books"):
			"при выборе вид вылетает из за отсутвия аттрибута selected_excel_books"
			if input_view_control.input_view.selected_excel_books != StatementConstants.all_tables_db:
				"если не сделать проверку будет слишком много табов сгенерено"
				return self.upload_layout.table_dict[input_view_control.input_view.selected_excel_books]
			else:
				return input_view_control.input_view.selected_excel_sheet
		else:
			"возвращаем выбранный вид"
			return table_name
