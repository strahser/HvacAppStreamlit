from Polygons.PolygonPlot.PolygonPlotlyControl import UploadLayout, pd, st, PlotView, PolygonPlotlyControl
from Session.StatementConfig import StatementConstants
import plotly.graph_objects as go

from library_hvac_app.StreamlitDownloadFunctions.DownloadPlotlyFigList import download_jpg_zip


class PlotToolsPanel:
	def __init__(self,
	             upload_layout: UploadLayout,
	             input_df: pd.DataFrame,
	             key,
	             ):
		self.upload_layout = upload_layout
		self.input_df = input_df
		self.key = key
		self.level_plots_session = st.session_state[StatementConstants.levels_plots]
		self.show_plots_checkbox = st.sidebar.checkbox("Show Plots", key=f"{self.key} show_plots")

	def create_plot_tools_panel(self):
		self._create_polygons_config()

	def _create_polygons_config(self):
		self.plot_view = PlotView(self.input_df, key=self.key)
		self.plot_view.get_plot_layout()
		self.level_name = self.plot_view.level_column_name
		self.level_list = self.input_df[self.level_name].unique().tolist()

	def create_plots(self, selected_table_value: list, clicked_filter_id_list=None):
		"""
			selected_table_value: for filtration
		"""
		# if self.is_need_show_plots:
		self.plotly_control = PolygonPlotlyControl(
			self.upload_layout,
			self.input_df,
			self.plot_view,
			merged_df_id=self.plot_view.unique_table_id
		)

		self.fig_list = self.plotly_control.plot_polygons_plot(
			self.level_list,
			column_filtered_list_id=selected_table_value,
			clicked_filter_id_list=clicked_filter_id_list
		)
		self._create_plot_sidebar()
		self._add_plot_to_session(self.fig_list)

	def _create_plot_sidebar(self):
		with st.sidebar:
			if self.fig_list:
				show_mini_plot_checkbox = st.checkbox("show mini plot")
				if show_mini_plot_checkbox:
					selected_level = st.selectbox("Select level", [val.level_name for val in self.fig_list])
					st.plotly_chart([val.plotly_fig for val in self.fig_list if val.level_name == selected_level][0],
						                use_container_width=True)

	def _add_plot_to_session(self, fig_list):
		for f in fig_list:
			self.level_plots_session[f.level_name] = f.plotly_fig.to_plotly_json()

	def create_download(self):
		if self.show_plots_checkbox:
			fig_list = [val.plotly_fig for val in self.fig_list]
			download_jpg_zip(fig_list)


def show_selected_levels(level_list: list[str])->None:
	st.subheader("Levels Plots")
	for level in level_list:
		f_html = st.session_state[StatementConstants.levels_plots][level]
		fig = go.Figure(data=f_html['data'], layout=f_html['layout'])
		with st.expander(level):
			st.write(fig, unsafe_allow_html=True)

