import pandas as pd
import streamlit as st
from SQL.SqlModel.SqlConnector import SqlConnector
from Networks.ControlNetwork.NetworkPressureLayout import NetworkPressureLayout
from Networks.NetworkViews.NetworkMainView import NetworkMainView
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import MenuChapters


def create_plot_layouts(network_main_view: NetworkMainView):
	json_polygons = st.session_state[StatementConstants.json_polygons]
	for config_view in network_main_view.network_config_view_list:
		main_network = NetworkPressureLayout(network_main_view, config_view, json_polygons)
		main_network.create_network_layout()
		main_network.create_new_plots()


def create_network_plot():
	session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
	json_polygons = st.session_state[StatementConstants.json_polygons]
	condition = "revit_export" in session_tables and "medium_property" in session_tables and len(json_polygons) > 1
	if condition:  # todo add user interface
		revit_export = pd.read_sql(f"select * from revit_export", con=SqlConnector.conn_sql)
		medium_property = pd.read_sql(f"select * from medium_property", con=SqlConnector.conn_sql)
		ducts_round = pd.read_sql(f"select * from ducts_round", con=SqlConnector.conn_sql)
		pipes = pd.read_sql(f"select * from pipes",	con=SqlConnector.conn_sql)
		input_settings_df = {"medium_property": medium_property, "ducts_round": ducts_round, "pipes": pipes}
		network_main_view = NetworkMainView(revit_export, input_settings_df,key=MenuChapters.Networks)
		network_main_view.create_layout(create_plot_layouts)