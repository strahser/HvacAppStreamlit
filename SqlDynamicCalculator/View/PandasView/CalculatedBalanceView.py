import pandas as pd
from Upload.UploadLayout import UploadLayout, ExcelSheetsDB
from library_hvac_app.pandas_custom_functions import group_subgroups
from SQL.SqlModel.SqlConnector import SqlConnector
import streamlit as st
from functools import reduce
import operator


class TableFilter:
	counter = 0

	def __init__(self, table: pd.DataFrame, key="filter_column"):
		type(self).counter += 1
		self.table = table
		self.key = key

	def __del__(self):
		type(self).counter -= 1

	def create_column_filter(self):
		filter_column = st.multiselect("Select Columns", self.table.columns, default=self.table.columns.to_list(),
		                               key=f"{self.key} {self.counter}")
		return filter_column


class SelectExcelList:

	def __init__(self, upload_layout: UploadLayout, list_sheet_name: list, df_list: list[pd.DataFrame], key=0):
		self.filter_column = None
		self.selected_df_table = None
		self.list_name = None
		self.key = key
		self.upload_layout = upload_layout
		self.list_sheet_name = list_sheet_name
		self.df_list = df_list

	def create_selected_excel_view(self):
		with st.expander("Select Excel Book and Sheet"):
			col1, col2 = st.columns([3, 8])
			with col1:
				loaded_book = [val for val in ExcelSheetsDB.loaded_excel_book if hasattr(self.upload_layout, val)]
				all_sheets = st.selectbox("Select Excel Book", loaded_book, key=f"all_sheets{self.key}")
				if hasattr(self.upload_layout, all_sheets):
					selected_sheet = st.selectbox("Select Excel Sheet", getattr(self.upload_layout, all_sheets),
					                              key=f"selected_sheet{self.key}")

					self.selected_df_table: pd.DataFrame = getattr(self.upload_layout, all_sheets)[selected_sheet]
			with col2:
				self.filter_column = TableFilter(self.selected_df_table, "selected view filter").create_column_filter()
				with st.expander("Selected Excel Sheet"):
					st.write(self.selected_df_table[self.filter_column])
			self.list_name = selected_sheet
			st.write("ALL Created Sheets in Session")
			st.write([val.list_name for val in st.session_state["list_sheet"]])
			add_to_session = st.button("Add To Session", key="Excel Sheets", )
			if add_to_session:
				self.list_sheet_name.append(self)
				self.df_list.append(self.selected_df_table[self.filter_column])
			return self.selected_df_table[self.filter_column]

	def _add_to_list_sheet(self):
		self.list_sheet_name.append(self)
		self.df_list.append(self.selected_df_table[self.filter_column])


class ShowAllSelectedSheets:

	def __init__(self, list_sheet: list[SelectExcelList], df_list: list[pd.DataFrame]):
		self.right_table = None
		self.left_table = None
		self.list_sheet = list_sheet  # list name
		self.df_list = df_list  # for zip list name

	def _get_one_table(self, col1, col2, key, table_alias="first_table"):
		with col1:
			left_table = st.selectbox(table_alias, [val.list_name for val in self.list_sheet],
			                          key=f"{table_alias}{key}")
		with col2:
			left_table = [df for val, df in zip(self.list_sheet, self.df_list)
			              if val.list_name == left_table][0]

			st.write(left_table)
		return left_table

	def show_config_table(self, key: str | int = 0, number_of_table=1, table_alias="first_table"):
		with st.expander("Show Tables"):
			col1, col2 = st.columns([3, 8])
			if number_of_table == 1:
				self.left_table = self._get_one_table(col1, col2, key, table_alias)
			if number_of_table == 2:
				self.left_table = self._get_one_table(col1, col2, key, "left table")
				self.right_table = self._get_one_table(col1, col2, key, "right table")


class ColumnOperation:
	counter = 0

	def __init__(self, list_sheet: list[SelectExcelList], df_list: list[pd.DataFrame]):
		type(self).counter += 1
		self.list_sheet = list_sheet
		self.df_list = df_list
		self.list_name = None

	def __del__(self):
		type(self).counter -= 1

	def _get_table(self, key: str | int = 0, number_of_table: int = 1, table_alias: str = "first_table"):
		show_table = ShowAllSelectedSheets(self.list_sheet, self.df_list)
		show_table.show_config_table(key, number_of_table, table_alias)
		return show_table

	def _add_to_session(self, table, alias: str = "New Table"):
		table_alias = st.text_input("Enter Table Alias", value=f"table alias {alias} {self.counter}",
		                            key=f" {alias} {self.counter}")
		self.list_name = table_alias
		filter_column = TableFilter(table, alias).create_column_filter()
		st.write(table[filter_column])
		add_to_session = st.button("Add To Session", key=alias)
		if add_to_session:
			self.list_sheet.append(self)
			self.df_list.append(table)
			st.success("Table In Session Created")
		self._add_table_to_db(table[filter_column], alias)
		return table[filter_column]

	@staticmethod
	def _add_table_to_db(selected_df_table: pd.DataFrame, key: str | int = 0):
		with st.expander("Add Table to DB"):
			db_table_name = st.text_input("Enter DB table name", value="new table", key=f"db_table_name{key}")
			button = st.button("Add table to DB?", key=f"button{key}")
			if button:
				try:
					selected_df_table.to_sql(db_table_name, SqlConnector.conn_sql, if_exists="replace")
					st.success(f"You add '{db_table_name}' table to DB")
					st.write(pd.read_sql_query(sql=f"""select * from {db_table_name}""", con=SqlConnector.conn_sql))
				except Exception as e:
					st.warning(e)


class MultiplyColumns(ColumnOperation):

	def __init__(self, list_sheet: list[SelectExcelList], df_list: list[pd.DataFrame]):
		super().__init__(list_sheet, df_list)

	def get_multiply_columns(self, key=0):
		with st.expander("Multiply Column"):
			table = self._get_table(key, 1, "multiply_table").left_table
			with st.expander("Select columns for Multiply"):
				columns = table.columns
				if isinstance(table, pd.DataFrame):
					multiply_columns = st.multiselect("Select Multiply  Columns", columns,
					                                  key=f"multiply_columns{key}")
					new_column = st.text_input("New Multiply Column", value="new column",
					                           key=f"get_multiply_columns{key}")

					try:
						df_list = [table[val] for val in multiply_columns]
						table[new_column] = reduce(operator.mul, df_list)
						table_filter = self._add_to_session(table, "Multiply Table")
						return table_filter
					except Exception as e:
						st.warning(e)


class SumColumns(ColumnOperation):
	def __init__(self, list_sheet: list[SelectExcelList], df_list: list[pd.DataFrame]):
		super().__init__(list_sheet, df_list)

	def sum_columns(self, key=1):
		key = self.counter
		with st.expander("Sum Column"):
			table = self._get_table(key).left_table
			with st.expander("Select columns for Sum"):
				sum_columns = st.multiselect("Select Sum Columns", table.columns, key=f"sum_columns{key}")
				new_column = st.text_input("New Sum Column", value="new column", key=f"sum_columns_view{key}")
				try:
					table[new_column] = table[sum_columns].sum(axis=1)
					table_filter = self._add_to_session(table, "Sum Table")
					return table_filter
				except Exception as e:
					st.warning(e)


class JoinTable(ColumnOperation):
	def __init__(self, list_sheet: list[SelectExcelList], df_list: list[pd.DataFrame]):
		"""create join view and call merge function"""
		super().__init__(list_sheet, df_list)
		self.right_table = None
		self.left_table = None

	def join_table(self, key=0) -> pd.DataFrame | None:
		table = self._get_table(key, 2, "join table")
		with st.expander("Select Data for joined table"):
			self.left_table = table.left_table
			self.right_table = table.right_table
			id_column1 = st.selectbox("Select ID column1", self.left_table.columns, key=f"id_column1{key}")
			id_column2 = st.selectbox("Select ID column2", self.right_table.columns, key=f"id_column2{key}")
			how = st.selectbox("Select Join type", ['left', 'right', 'outer', 'inner', 'cross'], key=f"how{key}")
			try:
				table = self.left_table.merge(self.right_table, left_on=id_column1, right_on=id_column2, how=how)
				table_filter = self._add_to_session(table, "Join Table")
				return table_filter
			except Exception as e:
				st.warning(e)


class CalculatedBalanceView:

	def __init__(self, upload_layout: UploadLayout, key=0):
		self.key = key
		self.upload_layout = upload_layout
		self.table = None
		self.add_to_session()
		self.list_sheet = st.session_state["list_sheet"]
		self.df_list = st.session_state["df_list"]

		selected_sheet = st.sidebar.checkbox("Select Sheet")
		join_table = st.sidebar.checkbox("Join Table")
		multiply_columns = st.sidebar.checkbox("Multiply Columns")
		sum_columns = st.sidebar.checkbox("Sum Columns")

		if selected_sheet:
			self._selected_sheet_view()
		if join_table:
			self._join_table_view()
		if multiply_columns:
			self._multiple_columns_view()
		if sum_columns:
			self._sum_columns_view()

	@staticmethod
	def add_to_session():
		if "list_sheet" not in st.session_state:
			st.session_state["list_sheet"] = []
		if "df_list" not in st.session_state:
			st.session_state["df_list"] = []

	def _selected_sheet_view(self):
		with st.expander("Selected Sheets"):
			excel_sheet = SelectExcelList(
				self.upload_layout, st.session_state["list_sheet"], st.session_state["df_list"], 0)
			excel_sheet.create_selected_excel_view()
			# st.session_state["list_sheet"] = []
			# st.session_state["df_list"] = []

	def _join_table_view(self):
		with st.expander("Join Table"):
			joined_table = JoinTable(self.list_sheet, self.df_list)
			joined_table.join_table()

	def _multiple_columns_view(self, key=0):
		df = MultiplyColumns(self.list_sheet, self.df_list)
		df.get_multiply_columns(key)

	def _sum_columns_view(self, key=0):
		df = SumColumns(self.list_sheet, self.df_list)
		df.sum_columns(key)

	@staticmethod
	def _create_group_table_view(selected_db, key=0) -> pd.DataFrame | None:
		with st.expander("Select Data for Group table"):
			grouped_columns = st.multiselect("Select group by columns", selected_db.columns,
			                                 key=f"grouped_columns{key}")
			agg_columns = st.multiselect("Select agg  columns", selected_db.columns, key=f"agg_columns{key}")
			agg_list = ["sum", "min", "max", "mean", "count"]
			agg_funk = st.multiselect("Select agg  function", agg_list, key=f"agg_funk{key}")
			group_table = CalculatedBalanceView.make_group_table(selected_db, grouped_columns, agg_columns, agg_funk)
			st.write("Grouped Table")
			columns = CalculatedBalanceView.create_column_filter(group_table)
			st.write(group_table[columns])
		return group_table[columns]

	@staticmethod
	def make_group_table(df: pd.DataFrame, grouped_columns: list[str], agg_columns: list[str],
	                     agg_funk) -> pd.DataFrame | None:
		try:
			if agg_funk:
				group_table = df.groupby(grouped_columns, as_index=False)[agg_columns].agg(agg_funk).reset_index()
				return group_table
			else:
				group_table = df.groupby(grouped_columns, as_index=False)[agg_columns].agg(sum).reset_index()
				return group_table
		except Exception as e:
			st.warning(e)

	@staticmethod
	def create_total_row(df: pd.DataFrame, key=0):
		with st.expander("Select Data for Add Total Row Table"):
			grouped_column = st.selectbox("Select Grouped Column", df.columns, key=f"grouped_column{key}")
			columns_list = st.multiselect("Select Main Column", df.columns, key=f"columns_list{key}")
			agg_column = st.selectbox("Select Aggregation Column", df.columns, key=f"agg_column{key}")
			total_name = st.text_input("Enter Total Row Name", value="Total", key=f"total_name{key}")
			try:
				pivot_surfaces = group_subgroups(df, grouped_column, columns_list, agg_column, total_name).reset_index()
				st.write(pivot_surfaces)
				st.write(pivot_surfaces[pivot_surfaces[columns_list].str.contains(total_name)])
				st.success(f"You Create '{total_name}' Table")
			except Exception as e:
				st.warning(e)
