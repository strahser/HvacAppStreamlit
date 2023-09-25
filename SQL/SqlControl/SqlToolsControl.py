import pandas as pd

from Components.EditableDataFrame.EditableDataFrameView import create_editable_df
from SQL.SqlControl.SqlDataSelectAndUpdateControl import SqlDataSelectAndUpdateControl
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputViewControl import InputViewControl
from SQL.SqlView.AddSQLTableView import AddSQLTableView
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
				df = create_editable_df(self.table_name, self.upload_layout, key="editable df")

				col = st.columns(3)
				with col[0]:
					new_view_table_name = st.text_input("Enter New View Table Name",
					                                         key=f"new_view_table_name {self.key} editable table")
					create_table_db_button = st.button("Create Table DB",
					                                        key=f"create_table_db button {self.key} editable table")
					from Session.UpdateDbSession import UpdateDbSession
					st.button("Update db", key=f"update_table_db button {self.key} editable table update",
					          on_click=UpdateDbSession.Update_sql_sessionData)
					if create_table_db_button:
						try:
							df_dicts = df.to_dict()
							pd.DataFrame(df_dicts).to_sql(new_view_table_name,if_exists="replace", con=self.connector)
							st.success(f"You create new table {new_view_table_name}")
						except Exception as e:
							st.warning(e)

	def _create_sql_tools(self):
		with st.sidebar:
			self.sql_table_control.create_sql_table_tools(self.selected_table_value)

	def _create_input_sql_tools_view(self):

		self.input_view_control = InputViewControl(self.upload_layout, self.key)
		self.input_view_control.create_input_view()
		self.input_df = self.input_view_control.input_df
		self.table_name = self.input_view_control.sheet_name
