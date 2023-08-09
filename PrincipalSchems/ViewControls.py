# region Import
import io
from InputView.InputViewControl import InputViewControl, UploadLayout
import numpy as np
from plotly import graph_objs as go
from PrincipalSchems.Models.Models import *
from PrincipalSchems.View.MainLayoutView import *
from Polygons.PolygonPlot.PolygonMerge import *
from Utility.TextWorker import TextWorkerForPlot
from datetime import datetime
from library_hvac_app.list_custom_functions import *


# endregion


# region Control
class WidgetsModelControl:
	"""
    StaticData class. Add distance and color to SystemProperty from widgets.
    """

	@staticmethod
	def add_start_widget_property(
			dict_df: dict,
			widget_instance: DynamicSystemView,
	) -> list[SystemProperty]:
		"""add distance and color to instance

        Args:
            dict_df (dict): _description_
            widget_instance (DynamicSystemView): _description_

        Returns:
            _type_: _description_
        """
		dict_df_ = dict_df.copy()
		sys_prop = []

		for key, val in dict_df.items():
			start_list = {}
			for val_id in val:
				if val_id:
					sys_property = SystemProperty()
					sys_property.space_id = key
					sys_property.system_name = val_id
					sys_property.distance_to_line = getattr(
						widget_instance, f"distance_{val_id}"
					)
					sys_property.color = getattr(widget_instance, f"color_{val_id}")
					start_list.update({val_id: sys_property})
					dict_df_[key] = start_list
					sys_prop.append(sys_property)
		return sys_prop

	@staticmethod
	def add_color_to_widget(widget_instance, sys_name):
		return getattr(widget_instance, f"color_{sys_name}")

	@staticmethod
	def create_and_add_property_to_system_property(input_df: pd.DataFrame, tabs_view1: TabsView):
		"""
        create SystemProperty and add
        """
		flow_columns = tabs_view1.system_and_flow_view.system_and_flow_view.flow_columns
		system_columns = tabs_view1.system_and_flow_view.system_and_flow_view.system_columns
		level_column = tabs_view1.static_layout.level_view_choose_column.level_column
		input_df = input_df.fillna(0)
		system_property_list: list[SystemProperty] = []
		wiget_instance = tabs_view1.dynamic_layout.system_view
		for flow, sys_name in zip(flow_columns, system_columns):
			for idx, row in input_df.iterrows():
				# add main property from input df
				sys_prop = SystemProperty()
				sys_prop.system_flow = row[flow]
				sys_prop.system_name = row[sys_name]
				sys_prop.space_id = row["S_ID"]
				sys_prop.level_value = row[level_column]
				# add color and distatnce
				if sys_prop.system_name != 0:
					sys_prop.distance_to_line = getattr(
						wiget_instance, f"distance_{sys_prop.system_name}"
					)
					sys_prop.color = getattr(
						wiget_instance, f"color_{sys_prop.system_name}"
					)
					sys_prop.vertical_direction_list = (
						tabs_view1.layout_view_context_data.vertical_direction_list
					)
					sys_prop.horizontal_direction_list = (
						tabs_view1.layout_view_context_data.horizontal_direction_list
					)
					system_property_list.append(sys_prop)
		return system_property_list

	@staticmethod
	def make_widget_group(input_df: pd.DataFrame, tabs_view1: TabsView):
		wiget_instance = tabs_view1.dynamic_layout.system_view
		system_property_list = (
			wiget_instance.create_and_add_propertys_to_system_property(
				input_df, tabs_view1
			)
		)
		# create df for grouping.
		df_wigets = pd.DataFrame({"wigets": system_property_list})
		df_wigets["space_id"] = df_wigets["wigets"].apply(lambda x: x.space_id)
		df_wigets = df_wigets.groupby("space_id")["wigets"].apply(list).reset_index()
		return df_wigets


class MainPointsCreatorControl:
	def __init__(
			self,
			input_df: pd.DataFrame,
			tab_view: TabsView,
			step_x: int = 50,
			step_y: int = 50,
	):
		# calculate start end points with layout data

		self.input_df = input_df.copy()
		self.layout_view_context_data = tab_view.layout_view_context_data
		self.tab_view = tab_view
		self.all_levels = input_df[self.layout_view_context_data.level_column]
		self.step_x = step_x
		self.step_y = step_y

	def _calculate_max_space_number_in_level(self) -> None:
		"""get maximum spaces on level. for calculate max point for vertical system line"""
		self.line_direction = self.layout_view_context_data.vertical_direction_list
		self.system_direction = self.layout_view_context_data.horizontal_direction_list
		self.max_space_count = (
			self.input_df.groupby(self.layout_view_context_data.level_column)["S_ID"]
			.count()
			.max()
		)

		return self.max_space_count

	def calculate_points(self):
		self._calculate_max_space_number_in_level()
		step = 0
		all_level_points = []
		shapely_polygons = []
		self.polygon_property = {}

		for level_ in self.all_levels.unique():
			filter_level_df = self.input_df.loc[self.all_levels == level_]

			df_dict = SystemGroupCreator.create_dictionary_from_df(
				filter_level_df, self.layout_view_context_data.main_columns
			)
			# df_property = WigetsModelControl.add_start_wiget_property(
			#     df_dict, dynamic_layout_view_context_data.base_property_wiget
			# )
			df_property = (
				WidgetsModelControl.create_and_add_property_to_system_property(
					self.input_df, self.tab_view
				)
			)
			polygon_main_model = PolygonMainModel(
				df_dict,
				step,
				self.max_space_count,
				step_x=self.step_x,
				step_y=self.step_y,
			)
			points_model = PointsMainModel(df_property, polygon_main_model)
			all_points = points_model.get_system_points(
				self.line_direction, self.system_direction
			)
			self.polygon_property.update(polygon_main_model.polygon_property)
			step += self.layout_view_context_data.level_distance

			all_level_points.append(all_points)
			shapely_polygons.append(polygon_main_model.polygon_dict.values())
		self.system_property_points: list[SystemProperty] = flatten(all_level_points)

		self.flatten_shapely_polygons = flatten(shapely_polygons)

		return self.system_property_points, self.flatten_shapely_polygons, self.polygon_property


class PolygonPointsMergeControl:
	def __init__(self, input_df: pd.DataFrame, tabs_view: TabsView) -> None:
		"""add start,end points,color from callback widgets  to df for plotting

        """
		self.input_df = input_df
		self.tabs_view = tabs_view
		self.layout_view_context_data = LayoutViewContextData(
			tabs_view.system_and_flow_view, tabs_view.static_layout
		)
		self.dynamic_layout_context_data = DynamicLayoutViewContextData(
			tabs_view.dynamic_layout
		)
		self.main_points_creator = MainPointsCreatorControl(
			self.input_df,
			self.tabs_view,
			step_x=self.layout_view_context_data.polygon_width,
			step_y=self.layout_view_context_data.polygon_height,
		)

	def get_level_property(self) -> list[LevelPropertyModel]:
		polygon_width = self.tabs_view.static_layout.space_dimension_view.polygon_width
		system_dist = self.tabs_view.static_layout.space_dimension_view.distance_between_systems
		vertical_direction_list = self.tabs_view.layout_view_context_data.vertical_direction_list
		level_x = polygon_width * self.main_points_creator.max_space_count / 2
		level_property_list: list[LevelPropertyModel] = []
		for level_ in self.main_points_creator.all_levels.unique():
			level_property = LevelPropertyModel()
			system_y = max([val.y_end_points for val in self.system_property_points if val.level_value == level_])
			level_property.system_y = system_y
			level_property.level_name = level_
			level_property.level_coord_x = level_x
			level_property.level_coord_y = system_y + system_dist
			level_property.vertical_direction_list = vertical_direction_list
			level_property_list.append(level_property)
		return level_property_list

	def _get_start_end_system_points(self) -> None:
		self.main_points_creator.calculate_points()
		self.system_property_points = self.main_points_creator.system_property_points

		flatten_shapely_polygons = self.main_points_creator.flatten_shapely_polygons
		self.polygon_dict = self.main_points_creator.polygon_property

	def _add_start_end_system_points_to_df(self) -> pd.DataFrame:
		df_system_property_points = pd.DataFrame(
			{
				"S_ID": [p.space_id for p in self.system_property_points],
				"system_name": [p.system_name for p in self.system_property_points],
				"p_x": [p.offset_point_x for p in self.system_property_points],
				"p_y": [p.offset_point_y for p in self.system_property_points],
			}
		)
		level_df = self.input_df[["S_ID", self.layout_view_context_data.level_column]]
		df_system_property_points_merge = df_system_property_points.merge(
			level_df, how="left", on="S_ID"
		)
		return df_system_property_points_merge

	def _get_system_points_between_levels(self) -> pd.DataFrame:
		df_level_points = (
			self._add_start_end_system_points_to_df()
			.groupby(["system_name"])
			.agg(
				Max_x=("p_x", np.max),
				Min_x=("p_x", np.min),
				Max_y=("p_y", np.max),
				Min_y=("p_y", np.min),
			)
			.reset_index()
		)
		return df_level_points

	def _add_system_color_to_df(
			self, dynamic_layout_view_context_data: DynamicLayoutViewContextData
	) -> pd.DataFrame:
		df_level_points = self._get_system_points_between_levels()
		df_level_points["color"] = df_level_points.apply(
			lambda df: WidgetsModelControl.add_color_to_widget(
				dynamic_layout_view_context_data.base_property_wiget, df["system_name"]
			),
			axis=1,
		)
		return df_level_points

	def _add_color_filter_to_df(self) -> pd.DataFrame:
		polygon_merge = PolygonMerge(
			self.input_df,
			self.polygon_dict,
			self.layout_view_context_data.space_data_view.color_filter_name,
		)
		merge_df = polygon_merge.merge_df()
		return merge_df

	def _add_text_to_df(self) -> TextWorkerForPlot:
		text_worker = TextWorkerForPlot(self._add_color_filter_to_df())
		pl_layout = self.layout_view_context_data.space_data_view
		text_worker.concat_value_with_prefix(
			pl_layout.space_prefix, pl_layout.space_suffix, pl_layout.space_value
		)
		return text_worker

	def calculate(self) -> None:
		self._get_start_end_system_points()
		self.add_color_df = self._add_system_color_to_df(
			self.dynamic_layout_context_data
		)
		self.merge_df = self._add_color_filter_to_df()
		self.df_text = self._add_text_to_df()
		self.system_list: list[
			pd.DataFrame
		] = self.dynamic_layout_context_data.unique_systems["system"].tolist()


class EquipmentPointLocationControl:
	def __init__(self, polygon_points_merge_control: PolygonPointsMergeControl):
		self.polygon_points_merge_control = polygon_points_merge_control

	def __create_equipment_location_point(
			self,
			system: str,
			level: str,
	) -> pd.DataFrame:
		"""create equipment new point(up or down point to exist level) or exist point(horizontal point)"""

		system_model = SystemLocationModelBase(
			self.polygon_points_merge_control.system_property_points,
			self.polygon_points_merge_control.input_df,
			system,
			level,
			self.polygon_points_merge_control.layout_view_context_data.level_column,
		)

		if system_model._is_equipment_level_in_system_level():
			exist_level_model = ExistLevelLocationModel(system_model)
			model_unique_level = exist_level_model.create_exist_level_equipment_base_point(
				self.polygon_points_merge_control.layout_view_context_data.horizontal_direction_list,
				self.polygon_points_merge_control.layout_view_context_data.equipment_horizontal,
			)
		else:
			new_level_model = NewLevelLocationModel(system_model)
			model_unique_level = new_level_model.add_create_equipment_location_to_df(
				self.polygon_points_merge_control.layout_view_context_data.equipment_vertical
			)
		return model_unique_level

	def get_location_point_list(
			self, level_list_value: DynamicWidgetsViewContextData._get_level_list_value
	) -> list:
		location_point_list = []
		for en, system in enumerate(self.polygon_points_merge_control.system_list):
			location_point = self.__create_equipment_location_point(system, level_list_value[en])
			location_point_list.append(location_point)
		return location_point_list


# endregion


# region Plotter
class PlotlyPlotter:
	def __init__(
			self, fig: go.Figure, polygon_points_merge_control: PolygonPointsMergeControl
	):
		self.fig = fig
		self._df = polygon_points_merge_control.df_text._df
		self.polygon_points_merge_control = polygon_points_merge_control
		self.level_property = polygon_points_merge_control.get_level_property()

	def add_level_text(self):
		for prop in self.level_property:
			if prop.vertical_direction_list == "up":
				self.fig.add_trace(
					# add flow
					go.Scatter(
						x=[prop.level_coord_x, prop.level_coord_x],
						y=[prop.level_coord_y, prop.level_coord_y],
						legendgroup="level name",
						name="level name",
						textfont=dict(size=18, family="Issocuper", color="black"),
						text=f"<em> {str(prop.level_name)} </em>",
						showlegend=False,
						mode="text",
					)
				)

	def add_text_to_plot(self):
		# text to center polygon
		self.fig.add_trace(
			go.Scatter(
				x=self._df["pcx"],
				y=self._df["pcy"],
				mode="text",
				textfont=dict(size=14, family="Issocuper", color="black"),
				text="<em>" + self._df["text"] + "</em>",
				texttemplate="%{text}",
				legendgroup="Space Text",
				name="Space Text",
				showlegend=False,
			)
		)

	def plot_vertical_side_plot_lines_to_system(self):
		# between levels
		for idx_, row in self.polygon_points_merge_control.add_color_df.iterrows():
			self.fig.add_trace(
				go.Line(
					x=(row["Max_x"], row["Min_x"]),
					y=(row["Max_y"], row["Min_y"]),
					line_color=row.color,
					legendgroup=row.system_name,
					name=row.system_name,
				)
			)

	def _plot_polygons_plot(
			self, show_color: bool = False, line_color_filter: str = False
	):

		for idx, row in self._df.iterrows():
			if show_color and line_color_filter:
				self.fig.add_trace(
					go.Scatter(
						x=row["px"],
						y=row["py"],
						fill="toself",
						line_color=row["color"],
						legendgroup=row[line_color_filter],
						name=row[line_color_filter],
						mode="lines",
						showlegend=True,
					)
				)
			else:
				self.fig.add_trace(
					go.Scatter(
						x=row["px"],
						y=row["py"],
						mode="lines",
						line_color="grey",
						showlegend=False,
					)
				)

	def plot_start_end_system_lines(self, textposition: str = "bottom left"):
		# from polygons up or down
		all_system_points = self.polygon_points_merge_control.system_property_points
		df_1 = pd.DataFrame([prop.__dict__ for prop in all_system_points])
		df_1 = df_1.groupby(['offset_point_x', 'offset_point_y'])["system_flow"].sum().reset_index()

		for point in all_system_points:
			self.fig.add_trace(
				# add flow
				go.Scatter(
					x=[point.x_start_points, point.x_start_points],
					y=[point.y_start_points, point.y_start_points],
					line_color=point.color,
					marker=dict(
						size=15,
						color=point.color,
						symbol="arrow-bar-down",
						# line=dict(width=0.5),
					),
					legendgroup=point.system_name,
					name=point.system_name,
					textfont=dict(size=14, family="Issocuper", color=point.color),
					text=f"<i> L={str(point.system_flow)} </i>",
					textposition=textposition,
					legendgrouptitle_text="Systems" + " " + point.system_name,
					showlegend=False,
					mode="text+markers",
				)
			)
			# add offset sum flow
			for idx, row in df_1.iterrows():
				if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
					self.fig.add_trace(
						# add sum flow
						go.Scatter(
							x=[point.offset_point_x, point.offset_point_x],
							y=[point.offset_point_y, point.offset_point_y],
							line_color=point.color,
							marker=dict(
								size=15,
								color=point.color,
								symbol="arrow-bar-down",
								# line=dict(width=0.5),
							),
							legendgroup=point.system_name,
							name=point.system_name,
							textfont=dict(size=16, family="Issocuper", color=point.color),
							text=f"<i> L {point.system_name} {point.level_value} = {round(row['system_flow'])} </i>",
							textposition=textposition,
							legendgrouptitle_text="Systems" + " " + point.system_name,
							showlegend=False,
							mode="text",
						)
					)

			self.fig.add_trace(
				# from polygons up or down
				go.Line(
					x=(point.x_start_points, point.x_end_points),
					y=(point.y_start_points, point.y_end_points),
					line_color=point.color,
					legendgroup=point.system_name,
					name=point.system_name,
					legendgrouptitle_text="Systems" + " " + point.system_name,
					showlegend=False,
					mode="lines+ text",
				)
			)
			# offset points
			self.fig.add_trace(
				go.Line(
					x=(point.x_end_points, point.offset_point_x),
					y=(point.y_end_points, point.offset_point_y),
					line_color=point.color,
					marker=dict(
						size=15,
						color=point.color,
						symbol="triangle-right",
						line=dict(width=0.6),
					),
					legendgroup=point.system_name,
					textfont=dict(size=14, family="Issocuper", color=point.color),
					name=point.system_name,
					text="<i>" + point.system_name + "</i>",
					textposition="bottom center",
					mode="lines+ markers+ text",
				)
			)

	def __plote_horizontal_line_to_equipment(self, row):
		self.fig.add_trace(
			go.Line(
				x=[row["base_point_x"], row["px"]],
				y=[row["base_point_y"], row["py"]],
				line_color=row["color"],
				legendgroup=row.system_name,
				name=row.system_name,
			)
		)

	def __text_check_position(
			self, base_point_x: float, base_point_y: float, px: float, py: float
	):
		"""check position for equipment text"""

		if base_point_x < px and base_point_y == py:
			return "middle left"
		elif base_point_x > px and base_point_y == py:
			return "middle right"
		elif base_point_x == px and base_point_y > py:
			return "top center"
		else:
			return "bottom center"

	def plot_add_text_to_equipment_point(
			self,
			dynamic_widgets_view_context_data: DynamicWidgetsViewContextData,
			location_point_list: list[pd.DataFrame],
	):

		for en, df in enumerate(location_point_list):  # levels iteration
			for idx_, row in df.iterrows():  # df row iteration
				# horizontal line to equipment
				self.__plote_horizontal_line_to_equipment(row)
			# equipment text and marker
			self.fig.add_trace(
				go.Scatter(
					x=df["base_point_x"],
					y=df["base_point_y"],
					legendgroup=dynamic_widgets_view_context_data.legend_group[en],
					name=dynamic_widgets_view_context_data.legend_group[en],
					text="<em>"
					     + df["system_name"].astype("string")
					     + " <br>"
					     + df[
						     self.polygon_points_merge_control.layout_view_context_data.level_column
					     ]
					     + " <br>"
					     + str(dynamic_widgets_view_context_data.flow_list_value[en])
					     + "</em>",
					textposition=self.__text_check_position(
						row["base_point_x"], row["base_point_y"], row["px"], row["py"]
					),
					textfont=dict(size=14, family="Issocuper"),
					mode="text+markers+lines",
					marker=dict(
						size=40,
						color=df.color,
						symbol=dynamic_widgets_view_context_data.equipment_symbol_list[
							en
						],
						line=dict(color="Black", width=2),
					),
				)
			)

	def __show_only_unique_legend(self):
		names = set()
		self.fig.for_each_trace(
			lambda trace: trace.update(showlegend=False)
			if (trace.name in names)
			else names.add(trace.name)
		)
		return self.fig

	def plot_update_fig(
			self,
			plot_height: float = 3000,
			plot_width: float = 3000,
			show_grid: bool = False,
			plote_titl: str = "Plot Title",
	) -> None:
		self.fig.update_traces(hoverinfo="text+name")

		self.fig.update_xaxes(
			showgrid=show_grid, zeroline=show_grid, showticklabels=show_grid
		)
		self.fig.update_yaxes(
			showgrid=show_grid,
			zeroline=show_grid,
			showticklabels=show_grid,
			scaleanchor="x",
			scaleratio=1,
		)
		self.fig.update_layout(
			margin={"r": 0, "t": 0, "l": 0, "b": 0},
			autosize=False,
			width=plot_height,
			height=plot_width,
			plot_bgcolor="rgba(0,0,0,0)",
			title={
				"text": f"<em> {plote_titl} </em>",
				"y": 0.9,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top",
			},
			title_font_size=20,
			title_font_family="Issocuper",
		)
		self.__show_only_unique_legend()


class DataForPlotting:
	def __init__(self, input_df: pd.DataFrame, tab: TabsView):
		self.dynamic_layout_context_data = DynamicLayoutViewContextData(
			tab.dynamic_layout
		)

		self.dynamic_widgets_view_context_data = DynamicWidgetsViewContextData(
			self.dynamic_layout_context_data
		)
		self.dynamic_widgets_view_context_data.calculate()
		self.polygon_points_merge_control = PolygonPointsMergeControl(input_df, tab)
		self.polygon_points_merge_control.calculate()
		self.equipment_location = EquipmentPointLocationControl(
			self.polygon_points_merge_control
		)
		self.location_point_list = self.equipment_location.get_location_point_list(
			self.dynamic_widgets_view_context_data.level_list_value
		)
		self.plot_title = tab.static_layout.plot_title


class PlotterCreateLayout:
	def __init__(self, fig, data_for_plotting: DataForPlotting) -> None:
		self.fig = fig
		self.data_for_plotting = data_for_plotting
		self.polygon_plotter_merge_control = (
			data_for_plotting.polygon_points_merge_control
		)

	def create_plote_layout(self, textposition: str = "bottom left"):
		plot_plotter = PlotlyPlotter(self.fig, self.polygon_plotter_merge_control)
		plot_plotter.plot_vertical_side_plot_lines_to_system()
		plot_plotter.plot_start_end_system_lines(textposition)
		plot_plotter._plot_polygons_plot(
			self.polygon_plotter_merge_control.layout_view_context_data.color_view_checkbox,
			self.polygon_plotter_merge_control.layout_view_context_data.space_data_view.color_filter_name,
		)
		plot_plotter.add_text_to_plot()
		plot_plotter.plot_add_text_to_equipment_point(
			self.data_for_plotting.dynamic_widgets_view_context_data,
			self.data_for_plotting.location_point_list,
		)
		plot_plotter.plot_update_fig(
			self.polygon_plotter_merge_control.layout_view_context_data.plot_height,
			self.polygon_plotter_merge_control.layout_view_context_data.plot_width,
			show_grid=False,
			plote_titl=self.data_for_plotting.plot_title,
		)
		plot_plotter.add_level_text()


# endregion


class SchemeMain:
	def __init__(self, upload_layout: UploadLayout, key):
		self.fig = go.Figure()
		self.upload_layout = upload_layout
		self.key = key

	def download_plt_html(self):
		# plt save
		buffer = io.StringIO()
		self.fig.write_html(buffer, include_plotlyjs="cdn")
		html_bytes = buffer.getvalue().encode()
		today = datetime.today().strftime('%Y-%m-%d')
		st.download_button(
			label="Download Plotly HTML",
			data=html_bytes,
			file_name="principal_schem" + today + ".html",
			mime="text/html",
		)

	@staticmethod
	def get_flow_text_direction(tabs_view: TabsView):
		if tabs_view.layout_view_context_data.vertical_direction_list == "up":
			return "top left"
		else:
			return "bottom left"

	@staticmethod
	def expander_equipment(tabs: TabsView):
		tabs.create_dynamic_equipment_layout()

	def tab_0(self, tabs: st.tabs):
		with tabs[0]:
			with st.expander("Hide/Show Input Data", True):
				input_view_control = InputViewControl(self.upload_layout, key=self.key)
				self.input_df = input_view_control.create_input_view()
				print("selected df",self.input_df)
				static_layout_view = StaticLayoutView(self.input_df, key=self.key)
				self.input_df.rename(
					columns={static_layout_view.ID_COLUMN: "S_ID"}, inplace=True
				)  # todo SID
				tabs_view1 = TabsView(static_layout_view, key=self.key)
				tabs_view2 = TabsView(static_layout_view, key=self.key, color_reverse=True)
				tabs_view1.create_choose_column_level()
				tabs_view1.create_choose_system_property(1, "first", uniq_key=f"{self.key} 1")
				tabs_view2.create_choose_system_property(2, "second", uniq_key=f"{self.key} 2")
		return tabs_view1, tabs_view2

	def tab_1(self, tabs: st.tabs, tabs_view1: TabsView, tabs_view2: TabsView):
		with tabs[1]:
			tabs_view1.create_space_dimensions()
		with tabs[4]:
			tabs_view1.add_plot_config()
		tab_view_list = [tabs_view1, tabs_view2]
		return tab_view_list

	def main(self):
		tabs = st.tabs(StaticTabsView.tabs)
		tabs_view1, tabs_view2 = self.tab_0(tabs)
		tab_view_list = self.tab_1(tabs, tabs_view1, tabs_view2)

		if tabs_view1.is_input_data_load() and tabs_view2.is_input_data_load():
			for tab in tab_view_list:
				with tabs[2]:
					tab.create_dynamic_equipment_layout()
				with tabs[3]:
					tab.create_dynamic_system_layout()
				data_for_plotting = DataForPlotting(self.input_df, tab)
				text_position = self.get_flow_text_direction(tab)
				plotter_create_layout1 = PlotterCreateLayout(self.fig, data_for_plotting)
				plotter_create_layout1.create_plote_layout(text_position)

		elif tabs_view1.is_input_data_load():
			with tabs[2]:
				self.expander_equipment(tabs_view1)
			with tabs[3]:
				tabs_view1.create_dynamic_system_layout()
				data_for_plotting1 = DataForPlotting(self.input_df, tabs_view1)
				plotter_create_layout1 = PlotterCreateLayout(self.fig, data_for_plotting1)
				text_position = self.get_flow_text_direction(tabs_view1)
				plotter_create_layout1.create_plote_layout(text_position)
		else:
			tabs_view1.waring_if_main_data_not_load()
		create_plot = st.button("Create Plot")
		if create_plot:
			self.download_plt_html()
			# plt_plotter_polygon = PltPolygonPlotter(fig_mpl, ax, data_for_plotting)
			# plt_plotter_polygon()
			# legend_without_duplicate_labels_fig(fig_mpl)
			# plt.legend()
			# st.pyplot(fig_mpl)
			# , use_container_width=True

			st.plotly_chart(self.fig)
