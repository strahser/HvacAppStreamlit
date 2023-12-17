import io
import zipfile

import pandas as pd
import streamlit as st
from Networks.CalculationNetwork.PressureCalculator.GetLongRoute import GetLongRoute
from Networks.ControlNetwork.CreateMainNetworkLayout import CreateMainNetworkLayout
from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Networks.NetworkViews.NetworkMainView import NetworkMainView
from Networks.PloteNetwork.NetworkPlotter import NetworkPlotter
from Networks.PloteNetwork.NetworkPressurePlotter import NetworkPressurePlotter
from Polygons.PolygonPlot.PolygonPlotter import save_plot_to_svg
from Session.StatementConfig import StatementConstants
from library_hvac_app.list_custom_functions import to_list


class NetworkPressureLayout:
	def __init__(self, network_main_view: NetworkMainView, network_config_view: NetworkConfigView, json_path: str):
		self.network_main_view = network_main_view
		self.network_config_view = network_config_view
		self.df_to_revit = network_main_view.df_to_revit
		self.json_path = json_path
		self.input_settings_df = network_main_view.input_settings_df
		self.network_layout = CreateMainNetworkLayout(network_main_view, network_config_view, json_path=json_path)
		self.network_layout.create_main_layout()
		self.system_name = self.network_main_view.system_name_choice
		self.level = self.network_config_view.level_value
		self.long_route_df_filter = None
		self.long_route_df = None
		self.df_pressure_concat = None
		self.df_pressure_concat_filter = None

	def _add_system_name_to_session(self):
		if self.system_name not in st.session_state[StatementConstants.network_plots]:
			st.session_state[StatementConstants.network_plots][self.system_name] = {}

	def create_network_layout(self):
		self.network_layout.create_main_layout()
		self.network_layout()

	def create_new_plots(self):
		self.create_pressure_df()
		self.add_data_to_session()

	@property
	def polygon_merge(self):
		from Polygons.PolygonPlot.PolygonMerge import PolygonMerge
		polygon_merge = PolygonMerge(
			self.df_to_revit,
			self.json_path,
			self.network_main_view.system_choice,
			self.network_main_view.level_column,
			self.network_config_view.level_value,
		)
		return polygon_merge

	def add_data_to_session(self) -> None:
		_fig1, _fig2, _fig3 = self._create_svg_from_fig()
		system_branch = NetworkBranchModel(system_level=self.level,
		                                   location_point=(
			                                   self.network_config_view.local_point_x,
			                                   self.network_config_view.local_point_y),
		                                   network_draft_plot_data=_fig1,
		                                   network_pressure_plot_data=_fig2,
		                                   network_long_plot_data=_fig3,
		                                   network_pressure_table=self.df_pressure_concat_filter.to_dict(),
		                                   network_long_pressure_table=self.long_route_df_filter.to_dict(),
		                                   system_name=self.system_name,
		                                   system_type=self.network_main_view.system_type_choice
		                                   )
		st.session_state[StatementConstants.network_plots][self.system_name][
			system_branch.branch_name] = system_branch.dict()
		st.session_state[StatementConstants.network_plots][self.system_name][
			"system_type"] = self.network_main_view.system_type_choice

	def _get_figures_for_layout(self) -> tuple[object, object, object]:
		height, weight = self.network_main_view.plot_height, self.network_main_view.plot_width
		self._add_system_name_to_session()
		self.create_pressure_long_route_df()
		_fig1 = self.create_network_plotter().calculate()
		_fig2 = self.create_pressure_plotter().calculate()
		_fig3 = self.create_pressure_long_route_plotter().calculate()
		_fig1.set_size_inches(weight, height)
		_fig2.set_size_inches(weight, height)
		_fig3.set_size_inches(weight, height)
		return _fig1, _fig2, _fig3

	def _create_svg_from_fig(self):
		_fig1, _fig2, _fig3 = self._get_figures_for_layout()  # plt object
		# svg object
		fig1 = save_plot_to_svg(_fig1)
		fig2 = save_plot_to_svg(_fig2)
		fig3 = save_plot_to_svg(_fig3)
		return fig1, fig2, fig3

	@staticmethod
	def get_concat_pressure_df(df_list):
		if len(df_list) > 1:
			return pd.concat(df_list)
		else:
			return df_list[0]

	@staticmethod
	def drop_center_rows_duplicates(df, prefix_from):
		prefix_from = to_list(prefix_from)
		for prefix_from in prefix_from:
			if prefix_from:
				df = df.drop(df[df["to"] == prefix_from + "cent"].index)
		return df

	# table
	def create_pressure_df(self):
		"""get calculated DF"""
		self.df_pressure_concat = self.get_concat_pressure_df(
			[val.concate_df() for val in self.network_layout.pressure_df_list]
		)
		self.df_pressure_concat_filter = self.df_pressure_concat \
			# .filter(FilteredNetworkData.filtered_columns)
		return self.df_pressure_concat_filter

	def create_pressure_long_route_df(self):
		long_route = GetLongRoute(self.df_pressure_concat)
		self.long_route_df = long_route.get_long_df()
		self.long_route_df_filter = self.long_route_df \
			# .filter(FilteredNetworkData.filtered_columns)
		return self.long_route_df_filter

	def create_network_plotter(self):
		network_plotter = NetworkPlotter(
			polygon_merge=self.network_layout.networks_update[0].polygon_merge,
			network_list=self.network_layout.networks_update,
			df_network=[
				network.df_branch for network in self.network_layout.networks_update
			],
			space_name=self.network_layout.network_main_view.space_name,
			is_filled=True,
		)
		return network_plotter

	def create_pressure_plotter(self):
		pressure_plotter = NetworkPressurePlotter(
			polygon_merge=self.network_layout.networks_update[0].polygon_merge,
			network_list=self.network_layout.networks_update,
			df_network=[
				val.drop_center_rows_dupblicates()
				for val in self.network_layout.add_layout_data_to_pressure_calculation()
			],
			title_prefix="Pressure Drop",
			show_grid=False,
		)
		return pressure_plotter

	def create_pressure_long_route_plotter(self):
		long_route_df = self.drop_center_rows_duplicates(
			self.long_route_df, self.network_layout.list_of_from
		)
		pressure_plotter_long_route = NetworkPressurePlotter(
			polygon_merge=self.network_layout.networks_update[0].polygon_merge,
			network_list=self.network_layout.networks_update,
			df_network=[long_route_df],
			title_prefix="Pressure Drop",
			show_grid=False,
		)
		return pressure_plotter_long_route

	@staticmethod
	def download_list_fig(file_name: str = "plot"):
		with io.BytesIO() as buffer:
			with zipfile.ZipFile(buffer, "w") as zip:
				for en, f_ in enumerate(st.session_state["Network Plots"]):
					# zip.writestr(f"{file_name}_{en + 1}.jpg", res1)
					zip.writestr(f"plot_{en + 1}.html", f_)
			buffer.seek(0)
			st.download_button(
				label="📥 Download Plots ZIP",
				data=buffer,  # StreamlitDownloadFunctions buffer
				file_name=f"{file_name}.zip"
			)
