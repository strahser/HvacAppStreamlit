import sqlite3

from Session.StatementConfig import StatementConstants
from SQL.SqlModel.SqlConnector import SqlConnector
import streamlit as st


class AddViewTableToSessionModel:
	def __init__(self, new_view_table_name: str,
	             sql_query: str,
	             create_view_db_button: bool,
	             new_category_name: str,
	             new_view_comments:str,
	             conn: sqlite3.Connection = SqlConnector.conn_sql):
		self.new_view_table_name = new_view_table_name
		self.sql_query = sql_query

		self.create_view_db_button = create_view_db_button
		self.new_category_name = new_category_name
		self.new_view_comments = new_view_comments
		self.conn = conn

	def create_sql_view_and_add_to_session(self, view=True):
		"""create st.session_state[StatementConstants.create_json][self.new_view_table_name] """
		if self.create_view_db_button:
			sql_view = self._choose_sql_view_or_table_query(view)
			try:
				self.conn.cursor().execute(sql_view)
				self.conn.commit()
				self._create_json_table_query_view(sql_view)
				# self._add_view_to_category_list(self.new_category_name, self.new_view_table_name)
				st.success(f"View Create") if view else st.success("Table Create")
			except Exception as e:
				st.warning(e)

	def _create_json_table_query_view(self, input_sql: str):
		""" create json in session"""
		st.session_state[StatementConstants.create_json][self.new_view_table_name] = {
			StatementConstants.sql_view_query: input_sql,
			StatementConstants.category_name: self.new_category_name,
			StatementConstants.view_name: self.new_view_table_name,
			StatementConstants.view_comments: self.new_view_comments,
		}

	@staticmethod
	def _add_view_to_category_list(category_name: str, view_name: str):
		views: dict = st.session_state[StatementConstants.table_db]
		if category_name not in views.keys():  # create empty category
			views[category_name] = []
		else:
			for category in views.keys():
				if category == category_name:
					if view_name not in views[category_name]:  # not in category values list
						views[category_name].append(view_name)
						st.success("you create table in category")
						st.write(f"category {category_name}: {views[category_name]}")
					else:
						views[category_name][:] = [view_name if x == view_name else x for x in views[category_name]]
						st.warning("you replace table in category")
						st.write(f"category {category_name}: {views[category_name]}")

	def _choose_sql_view_or_table_query(self, view=True):
		if view:
			return f"CREATE VIEW IF NOT EXISTS {self.new_view_table_name} AS {self.sql_query}"
		else:
			return f"CREATE TABLE IF NOT EXISTS {self.new_view_table_name} AS {self.sql_query}"