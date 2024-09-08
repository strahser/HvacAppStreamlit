from streamlit_tree_select import tree_select
import streamlit as st


def create_tree_select_view(nodes: list[dict], key):
	if key not in st.session_state:
		st.session_state[key] = {}
		if "checked" not in st.session_state[key]:
			st.session_state[key]["checked"] = []
	return tree_select(
		nodes, check_model="leaf", key=key,
		checked=st.session_state[key]["checked"])["checked"]


