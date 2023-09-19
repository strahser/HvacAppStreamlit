
import pandas as pd

from Components.EditableDataFrame.EditableDataFrameView import create_editable_df
from SQL.SqlControl.SqlDataSelectAndUpdateControl import SqlDataSelectAndUpdateControl
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputViewControl import InputViewControl
from Upload.UploadLayout import UploadLayout
import streamlit as st




class SqlToolsControl:
	def __init__(self, upload_layout: UploadLayout, key, connector=SqlConnector.conn_sql):
		self.upload_layout = upload_layout
		self.key = key
		self.connector = connector

	def create_sql_tools_panel(self):
		self._create_input_sql_tools_view()
		tab_agg, tab_df_editable = st.tabs(["Selected Table", "Excel like Table"])
		if self.table_name:
			with tab_agg:
				try:
					self.sql_table_control = SqlDataSelectAndUpdateControl(self.input_df, self.table_name)
					self.selected_table_value = self.sql_table_control.create_agg_table()
					self._create_sql_tools()
				except Exception as e:
					st.warning(e)
					self.selected_table_value = pd.DataFrame()
			with tab_df_editable:
				create_editable_df(self.table_name,self.upload_layout,key="editable df")


	def _create_sql_tools(self):
		with st.sidebar:
			self.sql_table_control.create_sql_table_tools(self.selected_table_value)

	def _create_input_sql_tools_view(self):

		self.input_view_control = InputViewControl(self.upload_layout, self.key)
		self.input_view_control.create_input_view()
		self.input_df = self.input_view_control.input_df
		self.table_name = self.input_view_control.sheet_name
