import streamlit as st
from Session.StatementConfig import StatementConstants


def get_session_system(system_name: str):
	return st.session_state[StatementConstants.network_plots].get(system_name)
