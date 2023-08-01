import ifcopenshell
import streamlit as st

import StaticData.CSS
from IFC.pages.Viewer import viewer_execute
from IFC.pages.quantities import quantities_execute
from streamlit_option_menu import option_menu


def callback_upload():
	st.session_state["file_name"] = st.session_state["uploaded_file"].name
	st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
	st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["array_buffer"].decode("utf-8"))
	st.session_state["is_file_loaded"] = True

	### Empty Previous Model Data from st.session_state State
	st.session_state["isHealthDataLoaded"] = False
	st.session_state["HealthData"] = {}
	st.session_state["Graphs"] = {}
	st.session_state["SequenceData"] = {}
	st.session_state["CostScheduleData"] = {}

	### Empty Previous DataFrame from st.session_state State
	st.session_state["DataFrame"] = None
	st.session_state["Classes"] = []
	st.session_state["IsDataFrameLoaded"] = False


def get_project_name():
	return st.session_state.ifc_file.by_type("IfcProject")[0].Name


def change_project_name():
	if st.session_state.project_name_input:
		st.session_state.ifc_file.by_type("IfcProject")[0].Name = st.session_state.project_name_input


def main():
	with st.sidebar:
		selected2 = option_menu(
			menu_title="IFC",
			options=["📁Loader", "🎮Viewer", "🧮Quantities"],
			icons=["", "", ""],
			menu_icon="cast",
			default_index=0,
			orientation="vertical",
			styles=StaticData.CSS.CssStyle.menu_styles
		)
	if selected2 == "📁Loader":
		st.subheader(""" 📁 Choose a file""")
		st.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload,
		                 label_visibility="collapsed")
		if "is_file_loaded" in st.session_state and st.session_state["is_file_loaded"]:
			st.success(f'Project successfuly loaded')
			st.write("🔃 You can reload a new file ")
	if selected2 == "🎮Viewer":
		viewer_execute()
	if selected2 == "🧮Quantities":
		quantities_execute()
