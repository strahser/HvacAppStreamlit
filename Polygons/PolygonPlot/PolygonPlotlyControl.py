from dataclasses import dataclass
from plotly import graph_objs as go
from Polygons.PolygonView.PlotView import *
from Utility.TextWorker import *
from Polygons.PolygonPlot.PolygonMerge import *
from Upload.UploadLayout import *


@dataclass()
class PlotlyFigList:
	plotly_fig: go.Figure
	level_name: str


class PolygonPlotlyControl:
	def __init__(self,
	             upload_layout: UploadLayout,
	             _df: pd.DataFrame,
	             plot_view: PlotView,
	             merged_df_id="S_ID"):
		self.upload_layout = upload_layout
		self.plot_view = plot_view
		self.merged_df_id = merged_df_id  # id for plot
		self._df = self._get_polygon_merge_list(_df)
		self.merge_df = self.__add_text_to_df()

	def plot_polygons_plot(self, level_list: list[str],
	                       column_filtered_list_id: pd.DataFrame = None,
	                       clicked_filter_id_list: list[str] = None,
	                       line_width=2
	                       ) -> list[PlotlyFigList]:
		self.fig_list = []

		for level_val in level_list:
			fig = go.Figure()
			filter_df = self.merge_df[self.merge_df[self.plot_view.level_column_name] == level_val]
			fig_values = self.plot_one_level(fig, filter_df, level_val, column_filtered_list_id,
			                                 clicked_filter_id_list,
			                                 line_width)

			with st.expander(f"{level_val}"):
				self.fig_list.append(fig_values)
		return self.fig_list


	def _get_polygon_merge_list(self, _df):
		polygon_merge = PolygonMerge(
			in_df=_df,
			geometry_data=self.upload_layout.json_file,
			color_filter_name=self.plot_view.color_filter_name,
			level_column=self.plot_view.level_column_name,
			merged_df_id=self.merged_df_id
		)
		return polygon_merge.merge_df()

	def __add_text_to_df(self):
		text_worker_for_plot = TextWorkerForPlot(self._df)
		return text_worker_for_plot. \
			concat_value_with_prefix(self.plot_view.space_prefix, self.plot_view.space_suffix,
		                             self.plot_view.space_value)

	@staticmethod
	def add_text_to_plot(fig: go.Figure, _df: pd.DataFrame):
		# add text to center polygon. _df- df with text(TextWorkerForPlot)
		fig.add_trace(
			go.Scatter(
				x=_df["pcx"],
				y=_df["pcy"],
				mode="text",
				textfont=dict(size=14, family="Issocuper", color="black"),
				text="<em>" + _df["text"] + "</em>",
				texttemplate="%{text}",
				legendgroup="Space Text",
				name="Space Text",
				showlegend=False,
				hovertemplate="Space Text"
			)
		)

	@staticmethod
	def __show_only_unique_legend(fig):
		names = set()
		fig.for_each_trace(
			lambda trace: trace.update(showlegend=False)
			if (trace.name in names)
			else names.add(trace.name)
		)
		return fig

	def __get_column_filter(self, column_filtered_list_id: pd.DataFrame) -> list:
		if not column_filtered_list_id.empty:
			column_filtered_list_id = column_filtered_list_id[self.plot_view.id_for_color_filter].values
			return [str(val) for val in column_filtered_list_id]

		else:
			return []

	@staticmethod
	def __get_clicked_filter(clicked_filter_id_list: list[str]):
		if clicked_filter_id_list:
			return [str(val) for val in clicked_filter_id_list]
		else:
			return []

	def __check_filter_mode(self, row: pd.Series,
	                        column_filtered_list_id: pd.DataFrame, clicked_filter_id_list: list[str]
	                        ):

		if self.plot_view.is_need_fill_color == "space fill color":
			return "toself"
		if self.plot_view.is_need_fill_color == "use clicked mouse color filter":
			column_filter = self.__get_column_filter(column_filtered_list_id)
			clicked_filter = self.__get_clicked_filter(clicked_filter_id_list)
			concat_filter = column_filter + clicked_filter
			if row[self.plot_view.id_for_color_filter] in concat_filter:
				return "toself"
		else:
			return None

	def plot_one_level(
			self, fig: go.Figure,
			filter_df: pd.DataFrame,
			level_val: str,
			column_filtered_list_id=pd.DataFrame(),
			clicked_filter_id_list=None,
			line_width=2) -> PlotlyFigList:
		clicked_filter_id_list = clicked_filter_id_list if clicked_filter_id_list else []
		for idx, row in filter_df.iterrows():
			x = row["px"]
			x.append(x[0])
			y = row["py"]
			y.append(y[0])
			fig.add_trace(
				go.Scatter(
					x=row["px"],
					y=row["py"],
					fill=self.__check_filter_mode(row, column_filtered_list_id, clicked_filter_id_list),
					line_color=row["color"],
					line_width=line_width,
					legendgroup=row[self.plot_view.color_filter_name],
					name=row[self.plot_view.color_filter_name],
					mode="lines",
					showlegend=True,
				)
			)
		self.add_text_to_plot(fig, filter_df)
		fig.update_xaxes(
			showgrid=False, zeroline=False, showticklabels=False
		)
		fig.update_yaxes(
			showgrid=False,
			zeroline=False,
			showticklabels=False,
			scaleanchor="x",
			scaleratio=1,
		)
		fig.update_layout(
			margin={"r": 0, "t": 0, "l": 0, "b": 0},
			autosize=False,
			width=1000,
			height=1000,
			plot_bgcolor="rgba(0,0,0,0)",
			title={
				"text": f"<em> {level_val} </em>",
				"y": 1,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top",
			},
			title_font_size=20,
			title_font_family="Issocuper",
		)
		fig_values = PlotlyFigList(fig, level_val)
		self.__show_only_unique_legend(fig)
		return fig_values

