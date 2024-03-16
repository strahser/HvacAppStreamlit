from StaticData.AppConfig import MenuChapters
from Session.StatementConfig import StatementConstants
import streamlit as st


class StatementInit:
    def __init__(self):
        self._add_table_and_views()
        self._add_json()
        self._load_app_session_state()
        self._save_selected_tables_names()
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
        if StatementConstants.network_plots not in st.session_state:
            st.session_state[StatementConstants.network_plots] = {}
        if StatementConstants.network_plots not in st.session_state:
            st.session_state[StatementConstants.network_plots] = {}
        if StatementConstants.networks not in st.session_state:
            st.session_state[StatementConstants.networks] = {}
        if StatementConstants.zones not in st.session_state:
            st.session_state[StatementConstants.zones] = {}

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
        if StatementConstants.view_sql_query_model not in st.session_state:
            st.session_state[StatementConstants.view_sql_query_model] = {}
        if StatementConstants.json_polygons not in st.session_state:
            st.session_state[StatementConstants.json_polygons] = {}

    @staticmethod
    def _add_table_and_views():
        if StatementConstants.table_db not in st.session_state:
            st.session_state[StatementConstants.table_db] = dict()
        if StatementConstants.all_tables_db not in st.session_state[StatementConstants.table_db].keys():
            st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db] = []
        if StatementConstants.all_tables_view not in st.session_state[StatementConstants.table_db].keys():
            st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view] = []
        if StatementConstants.category_view_list not in st.session_state:
            st.session_state[StatementConstants.category_view_list] = []
        if StatementConstants.category_dictionary not in st.session_state:
            st.session_state[StatementConstants.category_dictionary] = {}

    @staticmethod
    def _save_selected_tables_names():
        if StatementConstants.terminal_names_dict not in st.session_state:
            st.session_state[StatementConstants.terminal_names_dict] = dict()
        if StatementConstants.ahu_names_dict not in st.session_state:
            st.session_state[StatementConstants.ahu_names_dict] = dict()


StatementInit()
