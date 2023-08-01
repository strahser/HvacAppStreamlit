import streamlit as st
import sqlite3
import pandas as pd


class SheetsTabView:
	def __init__(self, tables_name: list[any], connection: sqlite3.Connection, key):
		"""create tab for every table with columns names"""
		self.connection = connection
		self.tables_name = tables_name
		self.key = key

	def choose_table_or_view_data(self):

		if isinstance(self.tables_name, list):
			tabs = st.tabs(self.tables_name)
			for en, table in enumerate(self.tables_name):
				self._create_tabs(table, tabs, en)
		elif isinstance(self.tables_name, str):
			self._write_df(table=self.tables_name)

	def _create_tabs(self, table: str, tabs: st.tabs, en: int = 0):
		try:
			with tabs[en]:
				self._write_df(table)
		except Exception as e:
			st.warning(e)

	def _write_df(self, table: str):
		col_names, col_df = st.columns([2, 7])
		with col_names:
			st.markdown(f"Columns of **{table}**")
			columns = pd.read_sql_query(f"select * from {table}", con=self.connection).columns
			st.write(columns)
		with col_df:
			st.markdown(f" **{table}**")
			df = pd.read_sql_query(f"SELECT * from {table}", con=self.connection)
			st.write(df)
