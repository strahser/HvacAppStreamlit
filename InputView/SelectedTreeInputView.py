
import streamlit as st
from StaticData.AppConfig import MenuChapters, StaticVariable
from Upload import UploadLayout
from Session.StatementConfig import StatementConstants
from library_hvac_app.html.TreeViewModel import get_tree_data_from_db, create_tree_select_view
from streamlit_tree_select import tree_select


class SelectedTreeInputView:
	def __init__(self, header: str, key):
		self.key = key
		self.header = header

	@staticmethod
	def _create_nodes():
		nodes_list = []

		for key, val in st.session_state[StatementConstants.table_db].items():
			if key != StatementConstants.all_tables_db:
				nodes = get_tree_data_from_db(label=key, data=val)
				nodes_list.append(nodes)
		return nodes_list

	def create_select_tree(self):
		nodes_list = self._create_nodes()
		selected_books = create_tree_select_view(nodes_list, self.key)
		if not isinstance(selected_books, str):
			return selected_books["checked"]
		else:
			return None
