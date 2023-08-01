from streamlit_plotly_events import plotly_events
from Polygons.Model.FilteredSelectedDataModel import FilteredSelectedDataModel
from Polygons.PolygonView.PlotlySelectByClickView import PlotlySelectByClickView
from Polygons.PolygonPlot.PolygonPlotlyControl import go, PlotView, PolygonPlotlyControl, pd, UploadLayout
from SQL.SqlControl.SQLFilteredTableControl import SQLFilteredTableControl


class ClickedSelectedControl:
	def __init__(self, input_df: pd.DataFrame, upload_layout: UploadLayout, plot_view: PlotView):
		self.input_df = input_df
		self.plot_view = plot_view
		self.sql_filter = SQLFilteredTableControl()
		self.upload_layout = upload_layout
	
	def __get_selected_values(self,
	                          column_filtered_list_id: pd.DataFram,
	                          clicked_filter_id_list: list[str],
	                          merged_df_id: str):
		"""with plot click event using"""
		self.plotly_control = PolygonPlotlyControl(
			self.upload_layout,
			self.input_df,
			self.plot_view,
			merged_df_id=merged_df_id)
		self.fig_list = self.plotly_control.plot_polygons_plot(column_filtered_list_id, clicked_filter_id_list)
		self.plotly_select_by_click_view = PlotlySelectByClickView(self.input_df, self.plot_view)
		check_fig_list = self._get_checking_fig_list()
		selected_values = plotly_events(check_fig_list[0] if check_fig_list else check_fig_list)
		return selected_values
	
	def _get_checking_fig_list(self):
		check_fig_list = []
		for val in self.fig_list:
			if val.level_name == self.plotly_select_by_click_view.level_names:
				check_fig_list.append(val.plotly_fig)
		return check_fig_list
	
	def _transform_coordinates_to_id(self, selected_values):
		filtered_selected_data = FilteredSelectedDataModel(
			self.plotly_control.merge_df,
			self.plot_view.level_column_name,
			self.plotly_select_by_click_view.level_names,
			self.plot_view.id_for_color_filter
		)
		selected_id = filtered_selected_data.get_selected_id(selected_values)
		self.sql_filter.insert_selected_id_to_sql_db("filtered_id_column", selected_id)
		if self.plotly_select_by_click_view.clear_selected:
			self.sql_filter.drop_table()
	
	def __create_plotly_level_event(self,
	                                column_filtered_list_id: pd.DataFrame = pd.DataFrame(),
	                                clicked_filter_id_list: list = None):
		"""create independent clickable plot"""
		filter_value_condition = self.plotly_control.merge_df[
			                         self.plot_view.level_column_name] == self.plotly_select_by_click_view.level_names
		selected_values = plotly_events(
			self.plotly_control.plot_one_level(
				go.Figure(),
				self.plotly_control.merge_df[filter_value_condition],
				self.plotly_select_by_click_view.level_names,
				column_filtered_list_id,
				clicked_filter_id_list
			).plotly_fig
		)
		return selected_values
