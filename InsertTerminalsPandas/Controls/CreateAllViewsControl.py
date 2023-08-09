import streamlit as st
import pandas as pd

from InsertTerminalsPandas.Core.DetailAggModel import get_level_filter_grid_df
from InsertTerminalsPandas.Controls.LevelPlotControl import CreateSelectedPlotsControl, CreateLevelPlots
from InsertTerminalsPandas.TermilalView.ConfigView import InputDataDF, ConfigView, LayoutOptions, ColumnChoosing
from InsertTerminalsPandas.TermilalView.DeviceCRUDView import DeviceCRUDView
from InsertTerminalsPandas.TermilalView.DownloadResulView import DownloadResulLayout
from InsertTerminalsPandas.Core.TerminalsDownloadResult import TerminalsDownloadResult


class CreateAllViewsControl:
	def __init__(self, input_data_df: InputDataDF, key):
		"""Create tabs"""
		self.key = key
		self.tabs_detail_view, self.tabs_config, self.tabs_main_plots, self.tabs_table_results, self.tabs_downloads = \
			st.tabs(["Detail View", "Config", "Plots", "Table Result", "Downloads"])
		self.input_data_df = input_data_df
		self.config_view = ConfigView(self.input_data_df, key=self.key)
		self.selected_id = []
		self.concat_all_level = None
		self.concat_level = None
		self.level_plot = None

	def choose_level_options(self):
		with self.tabs_config:
			self.config_view.create_config_tab()
		if self.config_view.choose_plot_radio_option == LayoutOptions.one_level:
			self.create_one_level_plot()
			self.create_download_tab(LayoutOptions.one_level)
		elif self.config_view.choose_plot_radio_option == LayoutOptions.detail_view:
			with self.tabs_detail_view:
				self.create_detail_view()
		elif self.config_view.choose_plot_radio_option == LayoutOptions.all_levels:
			self.create_all_levels_plots()
			self.create_download_tab(LayoutOptions.all_levels)

	def create_detail_view(self):
		"""create view,plot,tabel df for selected spaces"""

		device_crud = DeviceCRUDView(self.config_view.input_data_df)
		with st.sidebar:
			st.subheader('Show Type Data')
			show_revit_main_data_checkbox = st.checkbox('Show Spaces Data', key=f'{self.key} Show Spaces Data')
			show_device_checkbox = st.checkbox('Show system data', key=f'{self.key}Show system data', )
			show_data_checkbox = st.checkbox('Show device type Data', key=f'{self.key}Show device data')
		if show_revit_main_data_checkbox:
			st.subheader('Select level Spaces')
			with st.expander(''):
				self.selected_id = get_level_filter_grid_df(self.input_data_df.revit_export,
				                                            self.config_view.level_value)
		if show_device_checkbox:
			device_crud.create_devices_db_view()
		if show_data_checkbox:
			st.subheader("Device Type Data")
			st.write(device_crud.device_type_df)
		if self.selected_id:
			condition = self.input_data_df.revit_export[ColumnChoosing.S_ID].isin(self.selected_id)
			filter_df = self.input_data_df.revit_export[condition]
			selected_plot = CreateSelectedPlotsControl(self.config_view, filter_df, self.input_data_df)
			selected_plot.plot_selected_terminals_and_polygons(self.selected_id)
			with self.tabs_table_results:
				st.dataframe(selected_plot.create_selected_terminals_df())
			self.create_one_level_plot()
			self.create_download_tab(LayoutOptions.one_level)

	def create_one_level_plot(self) -> pd.DataFrame:
		self.level_plot = CreateLevelPlots(self.config_view, self.input_data_df.revit_export, self.input_data_df)
		self.level_plot.plot_all_polygons()
		self.level_plot.plot_terminals_from_joining_excel_input_data(self.config_view.level_value)
		with self.tabs_main_plots:
			self.level_plot.create_plot_results_layout()
		with self.tabs_table_results:
			self.level_plot.create_data_frame_results_layout()
		self.concat_level = self.level_plot.concat_all
		return self.concat_level

	def create_all_levels_plots(self) -> pd.DataFrame:
		concat_all_levels = []
		for level_ in self.config_view.df_levels:
			level_plot = CreateLevelPlots(self.config_view, self.input_data_df.revit_export, self.input_data_df)
			level_plot.plot_all_polygons()
			level_plot.plot_terminals_from_joining_excel_input_data(level_)
			with self.tabs_main_plots:
				level_plot.create_plot_results_layout()
			with self.tabs_table_results:
				level_plot.create_data_frame_results_layout()
			concat_all_levels.append(level_plot.concat_all)
		if concat_all_levels:
			self.concat_all_level = pd.concat(concat_all_levels, axis=0)
			return self.concat_all_level

	def create_download_tab(self, number_of_levels: str):
		if number_of_levels == LayoutOptions.one_level:
			with self.tabs_downloads:
				download_files = TerminalsDownloadResult(self.concat_level, self.input_data_df).create_download_data()
				DownloadResulLayout(download_files.excel_file, download_files.json_file).create_download_layout()

		if number_of_levels == LayoutOptions.all_levels:
			with self.tabs_downloads:
				download_files = TerminalsDownloadResult(self.concat_all_level,
				                                         self.input_data_df).create_download_data()
				DownloadResulLayout(download_files.excel_file, download_files.json_file).create_download_layout()