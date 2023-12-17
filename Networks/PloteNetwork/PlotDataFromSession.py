import numpy as np
import pandas as pd
import streamlit as st
from Networks.CalculationNetwork.StaticData.NetworkSessionConstants import NetworkSessionConstants
from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel
from Networks.NetworkModels.PressureModel import PressureModel
from Networks.PloteNetwork.FilteredNetworkData import FilteredNetworkData
from Networks.PloteNetwork.GraphPlot import visualise_graph
from Networks.Utils.NetworkSession import get_session_system
from Session.StatementConfig import StatementConstants


def get_root_temp_df_from_session(system: get_session_system, df_data: list):
	"""create df from session dict by system"""
	if system and system.get(NetworkSessionConstants.full_pressure_df):
		df_dict = system[NetworkSessionConstants.full_pressure_df]
		return pd.DataFrame.from_dict(df_dict)
	else:
		return pd.DataFrame(df_data)


def create_pressure_graph(system_name: str):
	system = get_session_system(system_name)
	with st.expander("Main Root Pressure Graph"):
		st.write(system[NetworkSessionConstants.graph_plot], unsafe_allow_html=True)
		st.subheader(f"{system_name} pressure loss")
		st.write(pd.DataFrame.from_dict(system[NetworkSessionConstants.full_pressure_df]))
		pressure_value = system[NetworkSessionConstants.calculated_pressure]
		flow_value = system[NetworkSessionConstants.calculated_flow]
		pressure = f"Full Pressure- {pressure_value}  Pa"
		flow = f"Full Flow- {flow_value} m3/h"
		st.write(pressure)
		st.write(flow)


def get_network_branch_model_from_session(system_name: str) -> list[NetworkBranchModel]:
	all_models = []
	data_to_dict = {}
	system = st.session_state[StatementConstants.network_plots][system_name]
	for key, systems in system.items():
		if key not in NetworkSessionConstants.excluding_list:
			for k, v in systems.items():
				data_to_dict[k] = v
			all_models.append(NetworkBranchModel(**data_to_dict))
	return all_models


def plot_data_from_session(system_name: str) -> list[NetworkBranchModel]:
	all_models = get_network_branch_model_from_session(system_name)
	try:
		create_pressure_graph(system_name)
	except:
		pass
	for model in all_models:
		if hasattr(model, "system_name"):
			with st.expander(model.branch_name):
				with st.expander(model.network_draft_plot_name):
					st.write(model.network_draft_plot_data, unsafe_allow_html=True)
				with st.expander(model.network_pressure_plot_name):
					st.write(model.network_pressure_plot_data, unsafe_allow_html=True)
					st.write(pd.DataFrame(model.network_pressure_table)
					         .filter(FilteredNetworkData.filtered_columns))
				with st.expander(model.network_long_plot_name):
					st.write(model.network_long_plot_data, unsafe_allow_html=True)
					st.write(pd.DataFrame(model.network_long_pressure_table)
					         .filter(FilteredNetworkData.filtered_columns)
					         )
	return all_models


def create_data_frame_from_session(network_plots: dict) -> dict[str, pd.DataFrame]:
	res_dict = {}
	for k, v in network_plots.items():
		res_dict[f"{k}_Полное давление "] = pd.DataFrame(network_plots[k].get(NetworkSessionConstants.full_pressure_df))
		models = get_network_branch_model_from_session(k)
		for model in models:
			res_dict[f"{model.branch_name}_магистраль"] = pd.DataFrame(model.network_long_pressure_table)
			res_dict[f"{model.branch_name}_ответвление"] = pd.DataFrame(model.network_pressure_table)
	return res_dict


def create_svg_from_session(network_plots: dict):
	res_dict = {}
	for k, v in network_plots.items():
		models = get_network_branch_model_from_session(k)
		res_dict[f"{k}_{NetworkSessionConstants.graph_plot}"] = network_plots[k].get(
			NetworkSessionConstants.graph_plot)
		for model in models:
			res_dict[f"{model.branch_name}_зонирование"] = model.network_draft_plot_data
			res_dict[f"{model.branch_name}_магистраль"] = model.network_pressure_plot_data
			res_dict[f"{model.branch_name}_магистраль_этаж"] = model.network_long_plot_data
	return res_dict


def create_main_root(system_name: str, input_settings_df: dict) -> pd.DataFrame:
	"""get system data from session. Create PressureModel """
	data_to_dict = {}
	pressure_df_data: [PressureModel] = []
	system = get_session_system(system_name)
	if system:
		# create NetworkBranchModel
		for key, systems in system.items():
			if key not in NetworkSessionConstants.excluding_list:
				for k, v in systems.items():
					data_to_dict[k] = v
				network_branch_model = NetworkBranchModel(**data_to_dict)
				pressure_model = PressureModel(system_type=network_branch_model.system_type,
				                               from_branch=network_branch_model.branch_name,
				                               to_branch=network_branch_model.system_level)
				pressure_model.additional_pressure = network_branch_model.max_pressure
				pressure_model.calculate_pressure(network_branch_model.max_flow, input_settings_df)
				pressure_df_data.append(pressure_model)
		# create central  models
		level_dict = system.get(NetworkSessionConstants.df_from_to_level)
		if pressure_df_data and level_dict:
			df_level_dict = pd.DataFrame(level_dict)
			df_level_dict[NetworkSessionConstants.system_type] = system["system_type"]
			pressure_model = list(PressureModel(*row) for row in df_level_dict.values)
			cum_sum = np.cumsum([val.flow for val in pressure_df_data + pressure_model])
			for en, p_model in enumerate(pressure_model):
				if p_model.flow:
					p_model.calculate_pressure(p_model.flow, input_settings_df)
				elif len(cum_sum) > en:
					p_model.calculate_pressure(cum_sum[en], input_settings_df)
				pressure_df_data.append(p_model)
			# create level  models
			pressure_df = pd.DataFrame(pressure_df_data)
			return pressure_df


def calculate_pressure_model_from_data_frame(system_name: str, df_from_session: pd.DataFrame,
                                             input_settings_df: dict) -> None:
	pressure_model_list = list(PressureModel(*row) for row in df_from_session.values)
	system = get_session_system(system_name)
	for model in pressure_model_list:
		model.calculate_pressure(model.flow, input_settings_df)
		if pressure_model_list is not None:
			system[NetworkSessionConstants.full_pressure_df] = pd.DataFrame(pressure_model_list).to_dict()


def add_main_root_to_session(df_from_session: pd.DataFrame, system_name: str) -> None:
	system = get_session_system(system_name)
	system[NetworkSessionConstants.full_pressure_df] = df_from_session.to_dict()
	visualise_graph(df_from_session, system_name)
