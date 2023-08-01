import pandas as pd
import streamlit as st
from SQL.SqlModel.SqlConnector import SqlConnector
from StaticData.AppConfig import StaticVariable
from streamlit_modal import Modal
from st_mui_dialog import st_mui_dialog
from Session.StatementConfig import StatementConstants


class UploadView:

	def get_upload_layout(self):
		st.subheader("Choose Excel or DB load")

		self.select_db_or_excel = st.radio(label="Choose Excel or DB load",
		                                   options=[StaticVariable.load_excel.value, StaticVariable.load_db.value],
		                                   horizontal=True,
		                                   label_visibility="collapsed")
		if self.select_db_or_excel == StaticVariable.load_excel.value:
			st.subheader("Choose  Excel Files")
			self.input_excel_sheet_uploader = st.file_uploader("Choose  Excel Files",
			                                                   accept_multiple_files=True,
			                                                   type=["xlsx", "xlsm"])
		else:
			st.subheader('Choose DB for update')
			self.upload_db = st.file_uploader("Choose DB for update", type="sql")
		st.subheader('Choose a JSON Polygons file for Plots')
		self.file_json_upload = st.file_uploader("Choose a JSON Polygons file", type="json")
		self.update_db_button = st.button("Update Data?", on_click=self.__create_pd_sql_table_query)
		self.__create_modal_window(key="DB All Tables Show")

	@staticmethod
	def __create_pd_sql_table_query():
		_all_tables_query = "SELECT * FROM sqlite_master where type='table'"
		_all_views_query = "SELECT name FROM sqlite_master WHERE type='view'"
		all_db_tables = pd.read_sql_query(_all_tables_query, con=SqlConnector.conn_sql)["name"].to_list()
		all_db_views = pd.read_sql_query(_all_views_query, con=SqlConnector.conn_sql)["name"].to_list()
		st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db] = all_db_tables
		st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view] = all_db_views
		return all_db_tables, all_db_views

	def __create_modal_window(self, key):
		modal = Modal("Upload DB Data", key=key, padding=100)
		open_modal = st.button("Show DB data", key=key)
		if open_modal:
			modal.open()
		if modal.is_open():
			with modal.container():
				col1, col2 = st.columns(2)
				col1.write("DB Tables")
				col1.write(st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db])
				col2.write("DB Views")
				col2.write(st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view])

	def __create_upload_modal(self):
		key = "Manual Modal Window"
		answer = st_mui_dialog(
			title="All DB Tables",
			content="\n,".join(self.all_db_tables),
			styling_open_button="""{"backgroundColor" :"lightgreen"}""",
			button_txt="Show Loaded Data Bases",
		)
