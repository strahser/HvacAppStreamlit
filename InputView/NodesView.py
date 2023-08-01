import streamlit as st
from InputView.CreateTreeSelectView import create_tree_select_view
from Session.StatementConfig import StatementConstants
from library_hvac_app.html.TreeViewModel import get_tree_data_from_db


class ViewNodes:
	def __init__(self, key):
		self.key = key
		self.tables_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		self.views_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]

	def _create_view_nodes(self):
		nodes_table = get_tree_data_from_db("Table data", self.tables_name)
		nodes_vew = get_tree_data_from_db("View data", self.views_name)
		return [nodes_table, nodes_vew]

	def create_tree_view_options(self, header: str):
		st.subheader(f"Select {header} data")
		nodes = self._create_view_nodes()
		self.table_tree = create_tree_select_view(nodes=nodes, key=self.key)
