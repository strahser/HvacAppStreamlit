from Session.StatementConfig import StatementConstants
from SQL.SqlModel.SqlConnector import SqlConnector
import streamlit as st


class CreateViewFromStatementModel:
	def __init__(self, conn=SqlConnector.conn_sql):
		if "create_json" not in st.session_state: st.session_state["create_json"] = None
		self.statement = st.session_state[StatementConstants.view_sql_query_model]
		self.conn = conn

	def parsing_session_statement(self) -> None:
		if self.statement:
			for key, val in self.statement.items():
				try:
					self.conn.cursor().executescript(val["sql_view_query"])
					st.success(f"Create {key} View Successful ")
				except Exception as e:
					del self.statement[key]
					st.warning(e)
