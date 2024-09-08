from dataclasses import dataclass

import streamlit as st
from Session.StatementConfig import StatementConstants


def without_keys(d: dict, keys: list[str]):
	return {k: v for k, v in d.items() if k not in keys}


@dataclass
class SelectDataDBModel:
	session_table_db: dict[str, list] = None
	loaded_db_tables_names: list = None
	loaded_db_views_names: list = None

	def __init__(self):
		self.session_table_db: dict[str, list] = without_keys(st.session_state[StatementConstants.table_db],
		                                                      [StatementConstants.all_tables_view])
		self.loaded_db_tables_names: list = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		self.loaded_db_views_names: list = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		self.all_loaded_db_views_and_tables: list = self.loaded_db_tables_names + self.loaded_db_views_names
