import streamlit as st
import pandas as pd
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Networks.NetworkViews.NetworkSystemView import NetworkSystemView
from Networks.PloteNetwork.PlotDataFromSession import plot_data_from_session
from Session.StatementConfig import StatementConstants


class NetworkMainView:
	def __init__(self, df_to_revit: pd.DataFrame, input_settings_df: dict):
		self.plot_width = None
		self.plot_height = None
		self.df_to_revit = df_to_revit
		self.input_settings_df = input_settings_df
		self.choose_existing_or_new_system = st.sidebar.radio("Choose Create o Exist", ["New System", "Exist System"])
		self.tabs = st.tabs(["System Options", "Network config", "Results", "Downloads"])
		self.network_config_view_list: list[NetworkConfigView] = []
		self.network_system_view = None

	def create_layout(self, create_plot_layouts):
		with self.tabs[0]:
			self.create_system_layout()
		with self.tabs[1]:
			level_list = self.network_system_view.level_list
			for level_index, level in enumerate(level_list):
				with st.expander(f"Network config {level}"):
					network_columns = st.columns(2)
					with network_columns[0]:
						network_config_view = NetworkConfigView(self.df_to_revit, self.network_system_view)
						network_config_view.create_network_layout(level_list, level_index)
						network_config_view.create_from_to_layout()
					with network_columns[1]:
						network_config_view.create_BranchPlotlyPlot()
				self.network_config_view_list.append(network_config_view)
		with self.tabs[2]:
			if self.choose_existing_or_new_system == "Exist System":
				selected_system = st.sidebar.selectbox("Select Existing System",
				                                       st.session_state[StatementConstants.network_plots].keys())
				plot_data_from_session(selected_system)
			if self.choose_existing_or_new_system == "New System":
				create_plots_button = st.sidebar.button("Create Plots", key="create_plots button")
				if create_plots_button:
					create_plot_layouts(self)
					plot_data_from_session(self.network_system_view.system_name_choice)
		with self.tabs[3]:
			if self.network_system_view.system_name_choice in st.session_state[StatementConstants.network_plots]:
				# self.create_df_and_plot_layout()
				pass

	def create_df_and_plot_layout(self):
		with st.expander(f'downloads'):
			st.download_button(label='📥 pressure tables',
			                   data=None,
			                   file_name="pandas_multiple.pdf")

	def create_system_layout(self):
		st.subheader("choose system options")
		with st.expander('choose system options'):
			self.network_system_view = NetworkSystemView(self.df_to_revit, self.input_settings_df)
			self.plot_width = st.number_input("Plot Width", value=15)
			self.plot_height = st.number_input("Plot Height", value=15, step=1)
			# condition_flow_not_nan = self.df_to_revit[self.network_system_view.sys_flow_choice].notna()
			# condition_flow_not_zero = self.df_to_revit[self.network_system_view.sys_flow_choice] != 0
			# self.df_to_revit.df_to_revit = self.df_to_revit[(condition_flow_not_nan) & (condition_flow_not_zero)]
		return self.network_system_view
