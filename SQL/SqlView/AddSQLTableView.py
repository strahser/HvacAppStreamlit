import streamlit as st

from Session.StatementConfig import StatementConstants
from Session.UpdateDbSession import UpdateDbSession
from library_hvac_app.list_custom_functions import to_list


class AddSQLTableView:
	def __init__(self, key):
		col1, col2, col3, col4 = st.columns(4)
		self.key = key

		with col1:
			self.create_view_db_button = st.button("Create View DB", key=f"create_view_db button {key}")
			self.create_table_db_button = st.button("Create Table DB", key=f"create_table_db button {key}")
			st.button("Update db", key=f"update_table_db button {key}", on_click=UpdateDbSession.Update_sql_sessionData)

		with col2:
			self.new_view_table_name = st.text_input("Enter New View Table Name", key=f"new_view_table_name {key}")
			self.new_view_comments = st.text_input("Enter Comments to view", key=f"new_view_comments {key}")

		with col3:
			self.category_name = self.__chose_category_type()

		with col4:
			self._add_category()

	def _add_category(self):
		category_name = st.text_input("Type new category name", value="Heat Balance", key=f"category name {self.key}")
		add_category_button = st.button("Add Category", key=f"add category button{self.key}")
		if add_category_button:
			category_view_list = st.session_state[StatementConstants.category_view_list]
			if category_name not in category_view_list:
				category_view_list.append(category_name)

	def __chose_category_type(self):
		category = to_list(st.session_state[StatementConstants.category_view_list])
		try:
			category_type = st.selectbox(
				"Select Category Type",
				category,
				key=f"category_type {self.key}"
			)
			return category_type
		except:
			return StatementConstants.without_category
