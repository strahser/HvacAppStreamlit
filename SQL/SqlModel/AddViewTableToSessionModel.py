import sqlite3

from Session.StatementConfig import StatementConstants
from SQL.SqlModel.SqlConnector import SqlConnector
import streamlit as st


class AddViewTableToSessionModel:
	def __init__(self, new_view_table_name: str, sql_query: str, add_to_category_button: bool,
	             create_view_db_button: bool, new_category_name: str, conn: sqlite3.Connection = SqlConnector.conn_sql):
		self.new_view_table_name = new_view_table_name
		self.sql_query = sql_query
		self.add_to_category_button = add_to_category_button
		self.create_view_db_button = create_view_db_button
		self.new_category_name = new_category_name
		self.conn = conn
	
	def create_sql_view_and_add_to_session(self, view=True):
		"""create st.session_state[StatementConstants.create_json][self.new_view_table_name] """
		
		if self.create_view_db_button and self._check_new_table_name():
			sql_view = self._choose_table_or_view(view)
			try:
				self.conn.cursor().execute(sql_view)
				self.conn.commit()
				st.session_state[StatementConstants.create_json][self.new_view_table_name] = {
					StatementConstants.sql_view_query: sql_view,
					StatementConstants.category_name: self.new_category_name,
					StatementConstants.view_name: self.new_view_table_name
				}
				st.success("View Create")
			except Exception as e:
				st.warning(e)
		elif not self._check_new_table_name():
			st.warning(f"{self.new_view_table_name} table name already exists, please choose another")
	
	def _choose_table_or_view(self, view=True):
		if view:
			return f"CREATE VIEW IF NOT EXISTS {self.new_view_table_name} AS {self.sql_query}"
		else:
			return f"CREATE TABLE  IF NOT EXISTS {self.new_view_table_name} AS {self.sql_query}"
	
	def _check_new_table_name(self):
		create_json = st.session_state[StatementConstants.create_json]
		if self.new_view_table_name not in create_json.keys():
			return True
		else:
			return False
