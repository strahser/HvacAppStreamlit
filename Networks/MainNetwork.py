import pandas as pd
import streamlit as st
import SQL.SqlModel.SqlConnector
from Networks.ControlNetwork.NetworkPressureLayout import NetworkPressureLayout
from Networks.NetworkViews.NetworkMainView import NetworkMainView
from Session.StatementConfig import StatementConstants


def create_network_plot():
	session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
	json_polygons = st.session_state[StatementConstants.json_polygons]
	condition = "revit_export" in session_tables and "medium_property" in session_tables and len(json_polygons) > 1
	if condition:  # todo add user interface
		revit_export = pd.read_sql(f"select * from revit_export", con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		medium_property = pd.read_sql(f"select * from medium_property", con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		network_main_view = NetworkMainView(revit_export, medium_property)
		network_main_view.create_layout()
		for config_view in network_main_view.network_config_view_list:
			main_network = NetworkPressureLayout(network_main_view, config_view,	json_polygons,)
			if main_network.network_layout.network_main_view.create_plots_button:
				main_network.create_network_layout()
				main_network.show_plots()