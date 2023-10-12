import dataclasses
import io
import zipfile
import streamlit as st
from dataclasses import dataclass, field
from Networks.ControlNetwork.CreateMainNetworkLayout import *
from Networks.NetworkModels.NetworkModel import NetworkBranchModel, NetworkSystemModel
from Networks.PloteNetwork.NetworkPressurePlotter import *
from Session.StatementConfig import StatementConstants
from library_hvac_app.DbFunction.pandas_custom_function import df_to_excel_in_memory


class FilteredNetworkData:
	filtered_columns = [
		"S_Name",
		"from",
		"to",
		"distance",
		"power",
		"flow",
		"diameter",
		"velocity",
		"line_pressure",
		"dinamic_pressure",
		"full_pressure",
	]


class NetworkPressureLayout:
	def __init__(self, network_main_view: NetworkMainView, network_config_view: NetworkConfigView, json_path: str):
		self.network_main_view = network_main_view
		self.network_config_view = network_config_view
		self.df_to_revit = network_main_view.df
		self.input_settings_df = network_main_view.input_settings_df
		self.network_layout = CreateMainNetworkLayout(network_main_view, network_config_view, json_path=json_path)
		self.network_layout.create_main_layout()
		self.system_name = self.network_main_view.network_system_view.system_name_choice
		self.level = self.network_config_view.network_level_view.level_val

	def _add_system_name_to_session(self):
		if self.system_name not in st.session_state[StatementConstants.network_plots]:
			st.session_state[StatementConstants.network_plots][self.system_name] = {}

	def create_network_layout(self):
		self.network_layout.create_main_layout()
		self.network_layout()

	@property
	def system_expander_name(self) -> str:
		system = self.network_main_view.network_system_view.system_name_choice
		level = self.network_config_view.network_level_view.level_val
		return f"System {system} {level}"

	def create_new_plots(self, plot_data_from_session):
		with self.network_layout.network_main_view.tabs[2]:
			with st.expander(self.system_expander_name):
				self.create_pressure_df()
				self.get_figures_for_layout()
				plot_data_from_session(self.system_name)

	def get_figures_for_layout(self) -> None:
		self._add_system_name_to_session()
		self.create_pressure_long_route_df()
		_fig1 = self.create_network_plotter().calculate()
		_fig2 = self.create_pressure_plotter().calculate()
		_fig3 = self.create_pressure_long_route_plotter().calculate()
		fig1 = self.get_saved_figures(_fig1)
		fig2 = self.get_saved_figures(_fig2)
		fig3 = self.get_saved_figures(_fig3)
		system_branch = NetworkBranchModel(system_level=self.level,
		                                   network_draft_plot_data=_fig1,
		                                   network_pressure_plot_data=_fig2,
		                                   network_long_plot_data=_fig3,
		                                   network_pressure_table=self.df_pressure_concate_filter,
		                                   network_long_pressure_table=self.longe_route_df_filter,
		                                   system_name=self.system_name,
		                                   system_type=self.network_main_view.network_system_view.system_type_choice
		                                   )
		all_systems_names = [val.branch_name for val in st.session_state[StatementConstants.network_plots][self.system_name] if hasattr(val, "branch_name")]
		st.write(all_systems_names)
		if system_branch.branch_name in all_systems_names:
			for en, val in enumerate(st.session_state[StatementConstants.network_plots][self.system_name]):
				if hasattr(val, "branch_name") and f"{self.system_name}_{self.level} == val.branch_name":
					st.session_state[StatementConstants.network_plots][self.system_name][en] = system_branch
		elif system_branch.branch_name not in all_systems_names:
			st.session_state[StatementConstants.network_plots][self.system_name].append(system_branch)

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
		self.df_pressure_concate = self.get_concat_pressure_df(
			[val.concate_df() for val in self.network_layout.pressure_df_list]
		)
		self.df_pressure_concate_filter = self.df_pressure_concate.filter(FilteredNetworkData.filtered_columns)
		return self.df_pressure_concate_filter

	def create_pressure_long_route_df(self):
		long_route = GetLongRoute(self.df_pressure_concate)
		self.longe_route_df = long_route.get_long_df()
		self.longe_route_df_filter = self.longe_route_df.filter(FilteredNetworkData.filtered_columns)
		return self.longe_route_df_filter

	# plots

	def create_network_plotter(self):
		network_plotter = NetworkPlotter(
			polygon_merge=self.network_layout.networks_update[0].polygon_merge,
			network_list=self.network_layout.networks_update,
			df_network=[
				network.df_branch for network in self.network_layout.networks_update
			],
			space_name=self.network_layout.system_layouts.space_name,
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
			self.longe_route_df, self.network_layout.list_of_from
		)
		pressure_plotter_long_route = NetworkPressurePlotter(
			polygon_merge=self.network_layout.networks_update[0].polygon_merge,
			network_list=self.network_layout.networks_update,
			df_network=[long_route_df],
			title_prefix="Pressure Drop",
			show_grid=False,
		)
		return pressure_plotter_long_route

	def get_saved_figures(self, fig) -> str:
		saved_figure1 = self.create_network_plotter().save_plot_to_svg(fig)
		return saved_figure1

	@staticmethod
	def download_list_fig(file_name: str = "plot"):
		with io.BytesIO() as buffer:
			with zipfile.ZipFile(buffer, "w") as zip:
				for en, f_ in enumerate(st.session_state["Network Plots"]):
					# zip.writestr(f"{file_name}_{en + 1}.jpg", res1)
					zip.writestr(f"plot_{en + 1}.html", f_)
			buffer.seek(0)
			btn = st.download_button(
				label="📥 Download Plots ZIP",
				data=buffer,  # StreamlitDownloadFunctions buffer
				file_name=f"{file_name}.zip"
			)

	def create_df_and_plot_layout(self):
		with st.expander(f'downloads {self.system_expander_name}'):
			# self.download_list_fig()
			df1 = self.df_pressure_concate_filter
			df2 = self.longe_route_df_filter
			buffer_list = df_to_excel_in_memory([df1, df2], ['sheet1', 'sheet2'])
			st.download_button(label='📥 pressure tables',
			                   data=buffer_list,
			                   file_name="pandas_multiple.xlsx", )
