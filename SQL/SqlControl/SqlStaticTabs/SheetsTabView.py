import streamlit as st
import sqlite3
import pandas as pd

from SQL.SqlView.AggTabelView import AggTabelView
from SqlDynamicCalculator.Controls.TableColumnsSelectorControl import TableColumnsSelectorControl


class SheetsTabView:
	def __init__(self, tables_name: list[any], connection: sqlite3.Connection, key):
		"""create tab for every table with columns names"""
		self.connection = connection
		self.tables_name = tables_name
		self.key = key

	def write_table_or_view_data(self):
		if isinstance(self.tables_name, list) and self.tables_name:
			tabs = st.tabs(self.tables_name)
			for en, table in enumerate(self.tables_name):
				self._create_tabs(table, tabs, en)

		elif isinstance(self.tables_name, str) and self.tables_name:
			self._write_df(table=self.tables_name)

	def _create_unique_column_data(self, selected_sheet):
		with st.expander("Select unique column data"):
			col = st.columns(3)
			try:
				df = pd.read_sql_query(f"select * from {selected_sheet}", con=self.connection)
				selected_column = col[0].multiselect("select column for checking", df.columns)
				df_list = []
				for data in selected_column:
					unique_column_data = pd.DataFrame({data: df[data].unique()})
					df_list.append(unique_column_data)
				st.write(pd.concat(df_list, axis=1).to_dict())
			except Exception as e:
				st.warning(e)

	def _create_tabs(self, table: str, tabs: st.tabs, en: int = 0):
		try:
			with tabs[en]:
				self._write_df(table)
				self._create_unique_column_data(table)
				selected_columns = TableColumnsSelectorControl(key=f' {table}')
				sql_columns = selected_columns.get_columns_for_query(table)
				st.write("Selected columns sql expiration")
				st.code(sql_columns, language='sql')
		except Exception as e:
			st.warning(e)

	def _write_df(self, table: str):
		st.markdown(f"Columns of **{table}**")
		table = pd.read_sql_query(f"select * from {table}", con=self.connection)
		columns = table.columns.unique().to_list()
		st.write(columns)
		with st.expander("Sample of table"):
			st.write(table)
