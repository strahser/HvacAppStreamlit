import streamlit as st
import sqlite3
import pandas as pd

from SQL.SqlView.AggTabelView import AggTabelView


class SheetsTabView:
	def __init__(self, tables_name: list[any], connection: sqlite3.Connection, key):
		"""create tab for every table with columns names"""
		self.connection = connection
		self.tables_name = tables_name
		self.key = key

	def choose_table_or_view_data(self):

		if isinstance(self.tables_name, list) and self.tables_name:
			tabs = st.tabs(self.tables_name)
			for en, table in enumerate(self.tables_name):
				self._create_tabs(table, tabs, en)
		elif isinstance(self.tables_name, str) and self.tables_name:
			self._write_df(table=self.tables_name)

	def _create_tabs(self, table: str, tabs: st.tabs, en: int = 0):
		try:
			with tabs[en]:
				self._write_df(table)
		except Exception as e:
			st.warning(e)

	def _write_df(self, table: str):
		st.markdown(f"Columns of **{table}**")
		table = pd.read_sql_query(f"select * from {table}", con=self.connection)
		columns = table.columns.unique().to_list()
		st.write(columns)
		with st.expander("Sample of table"):
			agg_table = AggTabelView(table)
			agg_table.create_filtered_table('sample of static table')

