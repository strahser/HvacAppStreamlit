import pandas as pd
import streamlit as st
import SQL.SqlModel.SqlConnector
from Networks.ControlNetwork.NetworkPressureLayout import NetworkPressureLayout
from Networks.NetworkViews.NetworkMainView import NetworkMainView
from Session.StatementConfig import StatementConstants


def show_existing_plots():
	return st.selectbox("Select Existing System", st.session_state[StatementConstants.network_plots].keys())


def plot_data_from_session(system_name: str):
	for systems in st.session_state[StatementConstants.network_plots][system_name]:
		if hasattr(systems, "system_name"):
			with st.expander(systems.network_draft_plot_name):
				st.write(systems.network_draft_plot_data, unsafe_allow_html=True)
			with st.expander(systems.network_pressure_plot_name):
				st.write(systems.network_pressure_plot_data, unsafe_allow_html=True)
				st.write(systems.network_pressure_table)
			with st.expander(systems.network_long_plot_name):
				st.write(systems.network_long_plot_data, unsafe_allow_html=True)
				st.write(systems.network_long_pressure_table)


def create_network_plot():
	session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
	json_polygons = st.session_state[StatementConstants.json_polygons]
	condition = "revit_export" in session_tables and "medium_property" in session_tables and len(json_polygons) > 1
	if condition:  # todo add user interface
		revit_export = pd.read_sql(f"select * from revit_export", con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		medium_property = pd.read_sql(f"select * from medium_property",
		                              con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		network_main_view = NetworkMainView(revit_export, medium_property)
		network_main_view.create_layout()
		choose_existing_or_new_system = st.sidebar.radio("Choose Create o Exist", ["New System", "Exist System"])
		create_plots_button = st.sidebar.button("Create Plots", key="create_plots button")
		if choose_existing_or_new_system == "Exist System":
			selected_plot = show_existing_plots()
			plot_data_from_session(selected_plot)
		if choose_existing_or_new_system == "New System":
			if create_plots_button:
				for config_view in network_main_view.network_config_view_list:
					main_network = NetworkPressureLayout(network_main_view, config_view, json_polygons)
					main_network.create_network_layout()
					main_network.create_new_plots(plot_data_from_session)
