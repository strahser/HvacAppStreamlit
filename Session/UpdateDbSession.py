from Session.StatementConfig import StatementConstants
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd
from streamlit_modal import Modal
from Session.StatementConfig import StatementConstants
import streamlit as st


class UpdateDbSession:
	@staticmethod
	def Update_sql_sessionData() -> tuple:
		_all_tables_query = "SELECT * FROM sqlite_master where type='table'"
		_all_views_query = "SELECT name FROM sqlite_master WHERE type='view'"
		all_db_tables = pd.read_sql_query(_all_tables_query, con=SqlConnector.conn_sql)["name"].to_list()
		all_db_views = pd.read_sql_query(_all_views_query, con=SqlConnector.conn_sql)["name"].to_list()
		st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db] = all_db_tables
		st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view] = all_db_views
		return all_db_tables, all_db_views

	@staticmethod
	def create_modal_window(key):
		modal = Modal("Upload DB Data", key=key, padding=100)
		open_modal_button = st.button("Show DB data", key=f"{key} open_modal_button button ")
		if open_modal_button:
			modal.open()
		if modal.is_open():
			with modal.container():
				col1, col2 = st.columns(2)
				col1.write("DB Tables")
				col1.write(st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db])
				col2.write("DB Views")
				col2.write(st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view])

	@staticmethod
	def update_table_list(table_name:str)->None:
		session_table_dict = st.session_state[StatementConstants.table_db]
		for key, val in session_table_dict.items():
			if isinstance(val, list):
				for v in val:
					if table_name == v:
						val.remove(v)
						session_table_dict[key] = val