from SQL.SqlModel.AddViewTableToSessionModel import *
from SQL.SqlView.AddSQLTableView import AddSQLTableView
import pandas as pd
from SQL.SqlView.CopyToClipBoardView import CopyToClipBoardView
from library_hvac_app.list_custom_functions import to_list


class SQLCreateViewPanel:
	def __init__(self, sql_query: str, key, conn: object = SqlConnector.conn_sql):
		"""update view from session statement. Add view query to session statement"""
		self.sql_query = sql_query
		self.conn = conn
		self.key = key
		self.create_table_db_button = None
		self.table_space_reserve = None
		self.st_query_code = None
		self.category_name = None
		self.new_view_table_name = None
		self.add_to_category_checkbox = None
		self.create_view_db_button = None
		self.check_button = None

	def show_sql_view_panel(self, show_sql=True):
		"""main view for create db view"""
		if show_sql:
			with st.expander("Show SQL Query"):
				"""dynamic SQL (st code)"""
				self.st_query_code = st.code(self.sql_query, language="sql")
				self.check_button = st.button("Check SQL", key=f"check button {self.key}")
				CopyToClipBoardView(self.st_query_code, self.conn, key=f" Dynamic SQL Copy {self.key}")
		else:
			self.check_button = st.button("Check SQL", key=f"check button {self.key}")
		self.table_space_reserve = st.empty()
		with st.expander("Create SQL Views"):
			data_view = AddSQLTableView(self.key)
			col1, col2, col3 = st.columns(3)
			self.create_view_db_button = data_view.create_view_db_button
			self.create_table_db_button = data_view.create_table_db_button
			self.new_view_table_name = data_view.new_view_table_name
			self.new_view_comments = data_view.new_view_comments
			with col2:
				self.category_name = data_view.category_name
		self._check_buttons()

	def _check_buttons(self):
		if self.check_button:
			self._show_sql_table(self.sql_query)
		if self.create_view_db_button:
			add_view_to_session = AddViewTableToSessionModel(self.new_view_table_name,
			                                                 self.sql_query,
			                                                 self.create_view_db_button,
			                                                 self.category_name,
			                                                 self.new_view_comments

			                                                 )
			add_view_to_session.create_sql_view_and_add_to_session(view=True)
		if self.create_table_db_button:
			add_view_to_session = AddViewTableToSessionModel(self.new_view_table_name,
			                                                 self.sql_query,
			                                                 self.create_table_db_button,
			                                                 self.category_name,
			                                                 self.new_view_comments
			                                                 )
			add_view_to_session.create_sql_view_and_add_to_session(view=False)

	def _show_sql_table(self, sql):
		try:
			with self.table_space_reserve:
				st.subheader("Sql DB Query Result")
				st.write(pd.read_sql(sql, self.conn))
		except Exception as e:
			st.warning(e)
