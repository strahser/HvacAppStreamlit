import streamlit as st
import pandas as pd
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Networks.NetworkViews.NetworkSystemView import NetworkSystemView


class NetworkMainView:
	def __init__(self, df: pd.DataFrame, input_settings_df: pd.DataFrame):
		self.df = df
		self.input_settings_df = input_settings_df
		self.tabs = st.tabs(["System Options", "Network config", "Results", "Downloads"])
		self.network_config_view_list: list[NetworkConfigView] = []
		self.network_system_view = None

	def create_layout(self):
		with self.tabs[0]:
			self.create_system_layout()
		with self.tabs[1]:
			level_list = self.network_system_view.level_list
			for level_index, level in enumerate(level_list):
				with st.expander(f"Network config {level}"):
					network_columns = st.columns(2)
					with network_columns[0]:
						network_config_view = NetworkConfigView(self.df, self.network_system_view)
						network_config_view.create_network_layout(level_list, level_index)
						network_config_view.create_from_to_layout()
					with network_columns[1]:
						network_config_view.create_BranchPlotlyPlot()
				self.network_config_view_list.append(network_config_view)

	def create_system_layout(self):
		st.subheader("choose system options")
		with st.expander('choose system options'):
			self.network_system_view = NetworkSystemView(self.df, self.input_settings_df)
		return self.network_system_view
