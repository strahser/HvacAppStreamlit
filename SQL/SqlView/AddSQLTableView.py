import streamlit as st


class AddSQLTableView:
	def __init__(self, key):
		col1, col2, col3 = st.columns(3)
		self.create_view_db_button = st.button("Create View DB", key=f"create_view_db button {key}")
		self.create_table_db_button = st.button("Create Table DB", key=f"create_table_db button {key}")
		with col1:
			self.add_to_category_checkbox = st.checkbox("Add To Category", value=True,
			                                          help="Category - HVAC category, Balance for example",
			                                          key=f"add_to_category_button {key}")
		with col2:
			self.new_view_table_name = st.text_input("Enter New View Table Name", key=f"new_view_table_name {key}")