from Polygons.PolygonView.SelectPlotView import SelectPlotView
from Polygons.PolygonsControl.PlotToolsPanel import UploadLayout, st, PlotToolsPanel, show_selected_levels
from Session.StatementConfig import StatementConstants
from library_hvac_app.StreamlitDownloadFunctions.DownloadPlotlyFigList import download_all_plt_html, download_jpg_zip
from SQL.SqlControl.SqlToolsControl import SqlToolsControl
import pandas as pd


class TabsPolygonSqlCreator:
	def __init__(self, upload_layout: UploadLayout, key: str) -> None:
		self.upload_layout = upload_layout
		self.key = key
		self.plot_view = None
		self.plotly_control = None
		self.select_by_click_view_data = None
		self.fig_list = None

	def _create_tab_list(self) -> None:
		all_tabs = st.tabs(["Input Table", "Plot Setting", "downloads"])
		self.change_input_table_tab, self.plot_setting_tab, self.downloads_tab = all_tabs

	def create_polygons_plot_and_tabs(self):
		self._create_tab_list()
		with self.change_input_table_tab:
			self._create_sql_tools_panel()
		with self.plot_setting_tab:
			self._create_plot_tools_panel()

		if self.plot_tools_panel.show_plots_checkbox:
			self.plot_tools_panel.create_plots(self.sql_tool.selected_table_value)
			show_selected_levels(self.plot_tools_panel.level_list)

		with self.downloads_tab:
			self._create_download_tab()

	def _create_sql_tools_panel(self):
		self.sql_tool = SqlToolsControl(self.upload_layout, key=self.key)
		self.sql_tool.create_sql_tools_panel()

	def _create_plot_tools_panel(self):
		self.plot_tools_panel = PlotToolsPanel(self.upload_layout,
		                                       self.sql_tool.input_df,
		                                       key=self.key,
		                                       )
		self.plot_tools_panel.create_plot_tools_panel()
	# 	self.sql_tool.selected_table_value

	def _create_download_tab(self):
		with self.downloads_tab:
			self.plot_tools_panel.create_download()
