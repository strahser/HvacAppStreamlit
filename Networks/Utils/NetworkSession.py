import streamlit as st
from Session.StatementConfig import StatementConstants
from typing import Any


def get_session_system(system_name: str) -> Any:
	"""return plot from session on None"""
	return st.session_state[StatementConstants.network_plots].get(system_name)
