import streamlit as st
import pandas as pd
from Networks.CalculationNetwork.StaticData.NetworkSessionConstants import NetworkSessionConstants
from Networks.NetworkViews.DownloadView import create_download_layout
from Networks.NetworkViews.FromToLevelView import FromToLevelView
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Networks.NetworkViews.NetworkMainViewComponents import NetworkMainViewComponents
from Networks.PloteNetwork.MiniPlotPolygons import MiniPlotPolygons
from Networks.PloteNetwork.PlotDataFromSession import plot_data_from_session, \
	add_main_root_to_session, create_main_root
from Networks.Utils.NetworkSession import get_session_system
from Networks.plote_polygons.MainBranchMiniPlotlyPlot import MainBranchMiniPlotlyPlot
from Polygons.PolygonPlot.PlotPlotlyUtils import PlotPlotlyUtils
from Session.StatementConfig import StatementConstants
from collections import defaultdict


class NetworkMainView(NetworkMainViewComponents):
	def __init__(self, df_to_revit: pd.DataFrame, input_settings_df: dict, key: str):
		super().__init__(df_to_revit, input_settings_df, key)

		self.network_config_view_list: list[NetworkConfigView] = []
		self.network_plots = st.session_state[StatementConstants.network_plots]

	def create_layout(self, create_plot_layouts):
		self._create_tab0()
		self._create_tab1()
		self._create_tab2(create_plot_layouts)
		self._create_tab3()

	def _create_tab0(self):
		with self.tabs[0]:
			self.create_system_view()

	def _create_tab1(self):
		def _create_miniplot():
			mini_plot = MiniPlotPolygons(self.df_to_revit, self.system_choice, self.sys_flow_choice,
			                             self.level_column)
			mini_plot.plot_one_level(level)
			filtered_df = mini_plot.level_filtered_df(level)
			condition = filtered_df[filtered_df[self.system_choice] == self.system_name_choice]
			df_flow = round(condition[self.sys_flow_choice].sum())
			PlotPlotlyUtils.add_text_to_plot(mini_plot.fig, filtered_df)
			mini_plot = MainBranchMiniPlotlyPlot(network_config_view, mini_plot.fig, df_flow)
			fig_ = mini_plot.create_mini_plots()
			try:
				st.write(fig_)
			except Exception as e:
				st.write(e)

		with self.tabs[1]:
			for level_index, level in enumerate(self.filtered_level_list):
				with st.expander(f"Network config {level}"):
					network_columns = st.columns([3, 2])
					with network_columns[0]:
						network_config_view = NetworkConfigView(self.df_to_revit, self.system_name_choice, self.key)
						network_config_view.create_network_layout(self.filtered_level_list, level_index)
						network_config_view.create_from_to_layout()
					with network_columns[1]:
						_create_miniplot()
				self.network_config_view_list.append(network_config_view)
			from_to_view = FromToLevelView(self.all_levels, self.system_name_choice, f"FromToLevelView {self.key}")
			try:
				from_to_view.create_table()
			except Exception as e:
				st.warning(e)
			try:
				system = st.session_state[StatementConstants.network_plots].get(self.system_name_choice)
				main_root_df = create_main_root(self.system_name_choice, self.input_settings_df)
				add_main_root_to_session(main_root_df, self.system_name_choice)
				system[NetworkSessionConstants.full_pressure_df] = main_root_df.to_dict()
				with st.expander("Main Root Pressure Graph"):
					st.write(system[NetworkSessionConstants.graph_plot], unsafe_allow_html=True)
			except Exception as e:
				st.warning(e)

	def _create_tab2(self, create_plot_layouts):
		def _show_existing_system():
			selected_system = st.sidebar.selectbox("Select Existing System", self.network_plots.keys())
			if selected_system:
				plot_data_from_session(selected_system)

		def _create_new_system(create_plot_layouts):
			create_plots_button = self.create_plots_button_component()
			condition = self.system_name_choice not in st.session_state[StatementConstants.network_plots]
			if create_plots_button:
				st.session_state[StatementConstants.network_plots][self.system_name_choice] = {}
				get_session_system(self.system_name_choice)
				main_root_df = create_main_root(self.system_name_choice, self.input_settings_df)
				add_main_root_to_session(main_root_df, self.system_name_choice)
				create_plot_layouts(self)
				plot_data_from_session(self.system_name_choice)

		with self.tabs[2]:
			if self.choose_existing_or_new_system == "Exist System":
				_show_existing_system()
			if self.choose_existing_or_new_system == "New System":
				_create_new_system(create_plot_layouts)

	def _create_tab3(self):
		with self.tabs[3]:
			if self.system_name_choice in self.network_plots:
				create_download_layout(self.network_plots)

	def create_system_view(self):
		st.subheader("choose system options")
		with st.expander('choose system options'):
			self.system_type_choice = self.system_type_component()
			self.system_choice = self.system_choice_component()
			self.sys_flow_choice = self.sys_flow_choice_component()
			self.level_column = self.level_column_component()
			self.system_name_choice = self.system_name_choice_component(self.system_choice)
			self.space_name = self.space_name_component()
			system_filter = self.df_to_revit[self.system_choice] == self.system_name_choice
			self.filtered_level_list = self.df_to_revit[system_filter][self.level_column].unique()
			self.all_levels = self.df_to_revit[self.level_column].unique()
			self.plot_width = self.plot_width_component()
			self.plot_height = self.plot_height_component()

	def __create_network_dictionary(self) -> dict:
		def_dict = defaultdict(list)
		for key, val in self.network_plots.items():
			def_dict["system_type"].append(self.network_plots[key].get('system_type'))
			def_dict["system"].append(key)
			def_dict["calculated_pressure"].append(self.network_plots[key].get('calculated pressure'))
			def_dict["calculated_flow"].append(self.network_plots[key].get('calculated flow'))
			if self.network_plots[key].get('full pressure df'):
				def_dict["diameter"].append(max(self.network_plots[key].get('full pressure df')["diameter"].values()))
			else:
				def_dict["diameter"].append(None)
		return def_dict

	def __write_plot_data(self, defaultdictionary: dict) -> None:
		st.write(pd.DataFrame(defaultdictionary))
		st.write(self.network_plots["C01"].get("system_type"))
		st.write(self.network_plots["C01"].get('calculated pressure'))
		st.write(self.network_plots["C01"].get('calculated flow'))
		st.write(max(self.network_plots["C01"]['full pressure df']["diameter"].values()))
