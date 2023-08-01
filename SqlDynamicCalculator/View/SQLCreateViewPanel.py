from SQL.SqlModel.AddViewTableToSessionModel import *
from SQL.SqlView.AddSQLTableView import AddSQLTableView
from SqlDynamicCalculator.CategoryDb import CategoryDb
import pandas as pd
from SQL.SqlView.CopyToClipBoardView import CopyToClipBoardView


class SQLCreateViewPanel:

	def __init__(self, sql_query: str, key, conn: object = SqlConnector.conn_sql):
		"""update view from session statement. Add view query to session statement"""
		self.sql_query = sql_query
		self.conn = conn
		self.key = key
		self.create_table_db_button = None
		self.table_space_reserve = None
		self.st_query_code = None
		self.category_type = None
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

			self.add_to_category_checkbox = data_view.add_to_category_checkbox
			self.new_view_table_name = data_view.new_view_table_name
			with col2:
				self.category_type = self.__chose_category_type()
		self._check_buttons()

	def _check_buttons(self):
		if self.check_button:
			self._show_sql_table(self.sql_query)
		if self.create_view_db_button:
			add_view_to_session = AddViewTableToSessionModel(self.new_view_table_name, self.sql_query,
			                                                 self.add_to_category_checkbox, self.create_view_db_button,
			                                                 self.category_type)
			add_view_to_session.create_sql_view_and_add_to_session()
		if self.create_table_db_button:
			add_view_to_session = AddViewTableToSessionModel(self.new_view_table_name, self.sql_query,
			                                                 self.add_to_category_checkbox, self.create_table_db_button,
			                                                 self.category_type)
			add_view_to_session.create_sql_view_and_add_to_session(False)

	def _check_new_table_name(self):
		condition = self.new_view_table_name and str(self.new_view_table_name) not in \
		            list(st.session_state[StatementConstants.create_json].keys())
		if condition:
			return True
		else:
			return False

	def __chose_category_type(self):
		if self.add_to_category_checkbox:
			category_list = list(CategoryDb.__annotations__.keys())
			category_type = st.selectbox("Select Category Type", category_list, key=f"category_type {self.key}")
			return category_type
		else:
			return StatementConstants.without_category

	def _show_sql_table(self, sql):
		try:
			with self.table_space_reserve:
				st.subheader("Sql DB Query Result")
				st.write(pd.read_sql(sql, self.conn))
		except Exception as e:
			st.warning(e)
