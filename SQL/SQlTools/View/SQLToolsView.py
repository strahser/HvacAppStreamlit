import pandas as pd
import streamlit as st
from st_mui_dialog import st_mui_dialog


class SQLToolsView:
	def __init__(self, init_df: pd.DataFrame):
		self.init_df = init_df

	def create_sql_tools_panel(self):
		with st.expander("SQL Tolls"):
			self.create_column_checkbox = st.checkbox("Add Column?")
			self.add_data_to_column_checkbox = st.checkbox("Add Data to Column?")
			self.delete_column_checkbox = st.checkbox("Delete Column?")
			self.delete_table_checkbox = st.checkbox("Delete Table?")
			self.update_input_date = st.button("update table")

	def create_column_view(self):
		self.create_column_button = st.button("create column")
		self.new_column_name = st.text_input("New Column Name", value="New_Column_Name")
		self.column_type = st.selectbox("Column type", ["TEXT", "INTEGER", "REAL", "BLOB"],
		                                key="select column type")

	def add_data_to_column_view(self):
		self.add_data_to_column_button = st.button("add data to column")
		self.changed_column = st.selectbox("select updated column name", self.init_df.columns.to_list(),
		                                   key="select updated column name")
		self.new_column_value = st.text_input("new column value", value="new column value")
		self.id_column = st.selectbox("select id column", self.init_df.columns.to_list(),
		                              key="select id column for db", help="""
									  select id column for filtering data in data base
									  """)

	def delete_column_view(self):
		self.delete_column_button = st.button("Delete column")
		self.delete_column_name = st.selectbox("select deleted column name", self.init_df.columns.to_list(),
		                                       key="select deleted column name")

	def show_columns_names_view(self):
		with st.expander("Existing Columns Names"):
			self.existing_columns = st.markdown(
				f"<b> existing columns </b> <br> {self.init_df.columns.to_list()}",
				unsafe_allow_html=True
			)

	def create_delete_tables_buttons(self):
		self.delete_view_db_button = st_mui_dialog(
			title="Confirmation Delete View",
			content="Please confirm that you want to delete View",
			button_txt="Delete View"
		)
		self.delete_table_db_button = st_mui_dialog(
			title="Confirmation Delete Table",
			content="Please confirm that you want to delete table",
			button_txt="Delete Table"
		)
