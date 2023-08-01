from StaticData.AppConfig import MenuChapters
from Session.StatementConfig import StatementConstants
import streamlit as st


class StatementInit:
	def __init__(self):
		self._add_table_and_views()
		self._add_json()
		self._load_app_session_state()
		if StatementConstants.loading_file not in st.session_state:
			st.session_state[StatementConstants.loading_file] = {}
		if StatementConstants.SimpleNamespace not in st.session_state:
			st.session_state[StatementConstants.SimpleNamespace] = ""
		if StatementConstants.levels_plots not in st.session_state:
			st.session_state[StatementConstants.levels_plots] = {}
		if StatementConstants.tableau_config not in st.session_state:
			st.session_state[StatementConstants.tableau_config] = None
		if StatementConstants.tableau_table not in st.session_state:
			st.session_state[StatementConstants.tableau_table] = ""
	@staticmethod
	def _load_app_session_state():
		if StatementConstants.mainHydralitMenuComplex not in st.session_state:
			st.session_state[StatementConstants.mainHydralitMenuComplex] = ""
		if StatementConstants.previous_view not in st.session_state:
			st.session_state[StatementConstants.previous_view] = ""
		if StatementConstants.selected_app not in st.session_state:
			st.session_state[StatementConstants.selected_app] = ""

	@staticmethod
	def _add_json():
		if f"{MenuChapters.analytics} {StatementConstants.select_join_table}" not in st.session_state:
			st.session_state[f"{MenuChapters.analytics} {StatementConstants.select_join_table}"] = ""
		if StatementConstants.create_json not in st.session_state:
			st.session_state[StatementConstants.create_json] = {}

	@staticmethod
	def _add_table_and_views():
		if StatementConstants.table_db not in st.session_state:
			st.session_state[StatementConstants.table_db] = dict()
		if StatementConstants.all_tables_db not in st.session_state[StatementConstants.table_db].keys():
			st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db] = []

		if StatementConstants.all_tables_view not in st.session_state[StatementConstants.table_db].keys():
			st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view] = []


StatementInit()
