import plotly.graph_objects as go
from Polygons.PolygonPlot.PolygonMerge import PolygonMerge
from Utility.TextWorker import TextWorkerForPlot
from Session.StatementConfig import StatementConstants
from Polygons.PolygonPlot.PlotPlotlyUtils import PlotPlotlyUtils
import streamlit as st


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