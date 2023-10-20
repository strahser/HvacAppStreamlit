import pandas as pd
import streamlit as st

from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel
from Networks.PloteNetwork.FilteredNetworkData import FilteredNetworkData
from Session.StatementConfig import StatementConstants


def plot_data_from_session(system_name: str) -> list[NetworkBranchModel]:
	data_to_dict = {}
	all_models = []
	for key, systems in st.session_state[StatementConstants.network_plots][system_name].items():
		for k, v in systems.items():
			data_to_dict[k] = v
		systems_from_dict = NetworkBranchModel(**data_to_dict)
		all_models.append(systems_from_dict)
		if hasattr(systems_from_dict, "system_name"):
			with st.expander(systems_from_dict.branch_name):
				with st.expander(systems_from_dict.network_draft_plot_name):
					st.write(systems_from_dict.network_draft_plot_data, unsafe_allow_html=True)
				with st.expander(systems_from_dict.network_pressure_plot_name):
					st.write(systems_from_dict.network_pressure_plot_data, unsafe_allow_html=True)
					st.write(pd.DataFrame(systems_from_dict.network_pressure_table)
					         .filter(FilteredNetworkData.filtered_columns))
				with st.expander(systems_from_dict.network_long_plot_name):
					st.write(systems_from_dict.network_long_plot_data, unsafe_allow_html=True)
					st.write(pd.DataFrame(systems_from_dict.network_long_pressure_table)
					         .filter(FilteredNetworkData.filtered_columns)
					         )
				st.write(systems_from_dict.max_pressure,systems_from_dict.max_flow)
	return all_models
