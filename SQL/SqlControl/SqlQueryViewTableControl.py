import streamlit as st

from AnalyticalTables.AnalyticalControls.PivotAndGroupTableControl import PivotAndGroupTableControl
from SQL.SqlControl.SqlStaticTabs.SqlStaticTabDataControl import SqlStaticTabDataControl
from SQL.SqlModel.SqlConnector import SqlConnector
from SQL.SqlView.CopyToClipBoardView import CopyToClipBoardView
from SqlDynamicCalculator.View.SQLCreateViewPanel import SQLCreateViewPanel
from SqlDynamicCalculator.AppSqlCalculator import SqlDynamicCalculator
from SQL.SqlView.QueryInputStaticTextView import QueryInputStaticTextView
from SQL.StaticExamplesSql import *
from SQL.SqlControl.SqlToolsControl import SqlToolsControl
from Upload.UploadLayout import UploadLayout


class SqlQueryViewTableControl:
	def __init__(self, upload_layout: UploadLayout, key, connector=SqlConnector.conn_sql):
		"""create sql_tools, static_sql_tab, dynamic_sql_tab"""
		self.upload_layout = upload_layout
		self.connector = connector
		self.key = key
		self.sql_tools, self.static_sql_tab,  self.example_tab = st.tabs(
			["SQL TOOLS", "StaticData SQL",  "Example"]
		)

	def create_all_query_view(self):
		with self.example_tab:
			self._create_example_query()
		with self.static_sql_tab:
			static_sql_tab_data = SqlStaticTabDataControl(self.upload_layout)
			static_sql_tab_data.create_sample_tables_db()
			add_table_tools = QueryInputStaticTextView()
			add_table_tools.create_input_text_query()
			config_view = SQLCreateViewPanel(add_table_tools.query_input, self.key)
			config_view.show_sql_view_panel(show_sql=False)
			CopyToClipBoardView(add_table_tools.query_input,self.connector,self.key)
		with self.sql_tools:
			self._create_sql_tools_panel()

	def _create_sql_tools_panel(self):
		self.sql_tool = SqlToolsControl(self.upload_layout, key=self.key)
		self.sql_tool.create_sql_tools_panel()
		st.subheader("Pivot table and Group Table Sample")
		self.pivot_and_group_table = PivotAndGroupTableControl()
		self.pivot_and_group_table.create_pivot_and_group_table(self.sql_tool.input_df,show_input_df=False)

	@staticmethod
	def _create_example_query():
		for example in SqlExample:
			with st.expander(example.value[0]):
				st.code(example.value[1])
