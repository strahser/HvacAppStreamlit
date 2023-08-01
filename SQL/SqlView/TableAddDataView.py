import pandas as pd
import streamlit as st



class TableAddDataView:
	def __init__(self, init_df: pd.DataFrame):
		self.init_df = init_df
	
	def update_view(self):
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
