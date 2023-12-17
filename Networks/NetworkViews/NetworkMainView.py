import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Networks.CalculationNetwork.StaticData.NetworkSessionConstants import NetworkSessionConstants
from Networks.NetworkViews.DownloadView import create_download_layout
from Networks.NetworkViews.FromToLevelView import FromToLevelView
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Networks.PloteNetwork.PlotDataFromSession import plot_data_from_session, \
	add_main_root_to_session, create_main_root
from Networks.Utils.NetworkSession import get_session_system
from Networks.plote_polygons.MainBranchMiniPlotlyPlot import MainBranchMiniPlotlyPlot
from Polygons.PolygonPlot.PlotPlotlyUtils import PlotPlotlyUtils
from Polygons.PolygonPlot.PolygonMerge import PolygonMerge
from Session.StatementConfig import StatementConstants
from Utility.TextWorker import TextWorkerForPlot
from library_hvac_app.list_custom_functions import to_list
from collections import defaultdict


class MiniPlotPolygons:

	def __init__(self, df, system_column_name, flow_column_name, level_column_name):
		self.json_polygons = st.session_state[StatementConstants.json_polygons]
		self.df = df
		self.color_filter_name = system_column_name
		self.flow_column_name = flow_column_name
		self.level_column_name = level_column_name
		# self.merged_df_id = merged_df_id
		self.fig = go.Figure()

	@property
	def polygon_merge_df(self):
		pm = PolygonMerge(
			in_df=self.df,
			geometry_data=self.json_polygons,
			color_filter_name=self.color_filter_name,
			level_column=self.level_column_name,
			# merged_df_id=merged_df_id
		)
		return pm.merge_df()

	def __add_text_to_df(self):
		text_worker_for_plot = TextWorkerForPlot(self.polygon_merge_df)
		return text_worker_for_plot.concat_value_with_prefix(" ,Q", "", [self.color_filter_name, self.flow_column_name])

	def level_filtered_df(self, level_val: str):
		return self.df[self.df[self.level_column_name] == level_val]

	def plot_one_level(self, level_val: str, line_width=2) -> None:
		self.df = self.__add_text_to_df()
		for idx, row in self.level_filtered_df(level_val).iterrows():
			x = row["px"]
			x.append(x[0])
			y = row["py"]
			y.append(y[0])
			self.fig.add_trace(
				go.Scatter(
					x=row["px"],
					y=row["py"],
					fill="toself",
					line_color=row["color"],
					line_width=line_width,
					legendgroup=row[self.color_filter_name],
					name=row[self.color_filter_name],
					mode="lines",
					showlegend=True,
				)
			)
			self.fig = PlotPlotlyUtils.show_only_unique_legend(self.fig)


class NetworkMainView:
	def __init__(self, df_to_revit: pd.DataFrame, input_settings_df: dict, key: str):
		self.df_to_revit = df_to_revit
		self.input_settings_df = input_settings_df
		st.sidebar.button("Refresh")
		self.create_plots_button = st.sidebar.button("Create Plots", key="create_plots button")
		self.choose_existing_or_new_system = st.sidebar.radio("Choose Create o Exist", ["New System", "Exist System"])
		self.tabs = st.tabs(["System Options", "Network config", "Results", "Downloads"])
		self.network_config_view_list: list[NetworkConfigView] = []
		self.network_plots = st.session_state[StatementConstants.network_plots]

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
		# st.write(pd.DataFrame(def_dict))
		# st.write(self.network_plots["C01"].get("system_type"))
		# st.write(self.network_plots["C01"].get('calculated pressure'))
		# st.write(self.network_plots["C01"].get('calculated flow'))
		# st.write(max(self.network_plots["C01"]['full pressure df']["diameter"].values()))
		self.key = key

	def create_layout(self, create_plot_layouts):
		with self.tabs[0]:
			self.create_system_view()
		with self.tabs[1]:
			for level_index, level in enumerate(self.filtred_level_list):
				with st.expander(f"Network config {level}"):
					network_columns = st.columns(2)
					with network_columns[0]:
						network_config_view = NetworkConfigView(self.df_to_revit, self.system_name_choice, self.key)
						network_config_view.create_network_layout(self.filtred_level_list, level_index)
						network_config_view.create_from_to_layout()
					with network_columns[1]:
						# mini plots
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
				self.network_config_view_list.append(network_config_view)
			from_to_view = FromToLevelView(self.all_levels, self.system_name_choice, f"FromToLevelView {self.key}")
			if st.session_state[StatementConstants.network_plots].get(self.system_name_choice):
				from_to_view.create_table()
				if from_to_view.add_table_to_session:
					system = st.session_state[StatementConstants.network_plots].get(self.system_name_choice)
					main_root_df = create_main_root(self.system_name_choice, self.input_settings_df)
					try:
						add_main_root_to_session(main_root_df, self.system_name_choice)
						system[NetworkSessionConstants.full_pressure_df] = main_root_df.to_dict()
						with st.expander("Main Root Pressure Graph"):
							st.write(system[NetworkSessionConstants.graph_plot], unsafe_allow_html=True)
					except Exception as e:
						st.warning(e)
		with self.tabs[2]:
			if self.choose_existing_or_new_system == "Exist System":
				selected_system = st.sidebar.selectbox("Select Existing System", self.network_plots.keys())
				if selected_system:
					plot_data_from_session(selected_system)
			if self.choose_existing_or_new_system == "New System":
				if self.create_plots_button:
					if self.system_name_choice not in st.session_state[StatementConstants.network_plots]:
						st.session_state[StatementConstants.network_plots][self.system_name_choice] = {}
					try:
						get_session_system(self.system_name_choice)
						main_root_df = create_main_root(self.system_name_choice, self.input_settings_df)
						add_main_root_to_session(main_root_df, self.system_name_choice)
					except Exception as e:
						st.warning(e)
					create_plot_layouts(self)
					plot_data_from_session(self.system_name_choice)
		with self.tabs[3]:
			if self.system_name_choice in self.network_plots:
				create_download_layout(self.network_plots)

	def create_system_view(self):
		st.subheader("choose system options")
		with st.expander('choose system options'):
			self.system_type = self.input_settings_df["medium_property"]["system_type"].unique()
			self.system_type_choice = st.selectbox("choose system type", to_list(self.system_type),
			                                       key=f"system_type_choice {self.key}")
			self.system_choice = st.selectbox("choose system column", to_list(self.df_to_revit.columns),
			                                  key=f"system_choice {self.key}")
			self.sys_flow_choice = st.selectbox("choose flow column", to_list(self.df_to_revit.columns),
			                                    key=f"sys_flow_choice {self.key}")
			self.level_column = st.selectbox("choose level column", to_list(self.df_to_revit.columns),
			                                 key=f"level_column {self.key}")
			self.system_name_choice = st.selectbox("choose system", self.df_to_revit[self.system_choice].unique(),
			                                       key=f"system_name_choice {self.key}")
			self.space_name = st.selectbox(
				"Select additional space  name text",
				["S_ID", "S_Name", "S_Number"],
				index=2,
				key=f"space_name {self.key}")  # todo delete hardcode
			system_filter = self.df_to_revit[self.system_choice] == self.system_name_choice
			self.filtred_level_list = self.df_to_revit[system_filter][self.level_column].unique()
			self.all_levels = self.df_to_revit[self.level_column].unique()
			self.plot_width = st.number_input("Plot Width", value=15, key=f"plot_width {self.key}")
			self.plot_height = st.number_input("Plot Height", value=15, step=1, key=f"plot_height {self.key}")
