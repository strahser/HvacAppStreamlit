from typing import Any

import pandas as pd
import streamlit as st

from InputView.InputViewMultyChoosing import InputViewMultyChoosing
from SQL.SqlModel.SqlConnector import SqlConnector
from Networks.ControlNetwork.NetworkPressureLayout import NetworkPressureLayout
from Networks.NetworkViews.NetworkMainView import NetworkMainView
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import MenuChapters
from Upload.UploadLayout import UploadLayout


def create_plot_layouts(network_main_view: NetworkMainView):
	json_polygons = st.session_state[StatementConstants.json_polygons]
	for config_view in network_main_view.network_config_view_list:
		main_network = NetworkPressureLayout(network_main_view, config_view, json_polygons)
		main_network.create_network_layout()
		main_network.create_new_plots()


def create_network_plot(upload_layout: UploadLayout, key: str):
	input_view = InputViewMultyChoosing(upload_layout, key=f'{key} network load data')
	input_view.check_input_data_loaded(
		['revit_export', 'medium_property', 'ducts_round', 'pipes'],
		StatementConstants.networks
	)
	json_polygons = st.session_state[StatementConstants.json_polygons]
	network_dict_constant = st.session_state[StatementConstants.networks]
	condition1 = "" if network_dict_constant.get('revit_export') else "revit_export not load"
	condition2 = "" if network_dict_constant.get('medium_property') else "medium_property not load"
	condition3 = "" if len(json_polygons) > 1 else "json_polygons not load"
	condition = network_dict_constant.get('revit_export') \
	            and network_dict_constant.get("medium_property") \
	            and len(json_polygons) > 1
	if condition:
		revit_export = pd.read_sql("select * from revit_export", con=SqlConnector.conn_sql)
		medium_property = pd.read_sql("select * from medium_property", con=SqlConnector.conn_sql)
		ducts_round = pd.read_sql("select * from ducts_round", con=SqlConnector.conn_sql)
		pipes = pd.read_sql("select * from pipes", con=SqlConnector.conn_sql)
		input_settings_df = {"medium_property": medium_property, "ducts_round": ducts_round, "pipes": pipes}
		network_main_view = NetworkMainView(revit_export, input_settings_df, key=MenuChapters.Networks)
		network_main_view.create_layout(create_plot_layouts)
	else:
		message = ' ,'.join([condition1, condition2, condition3])
		st.warning(f"please check: {message}")
