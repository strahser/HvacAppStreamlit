import io
from matplotlib import pyplot as plt
from datetime import datetime
import streamlit as st
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


def legend_without_duplicate_labels_ax(ax):
	handles, labels = ax.get_legend_handles_labels()
	unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
	ax.legend(*zip(*unique), fontsize=20)


def legend_without_duplicate_labels_fig(figure):
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = dict(zip(labels, handles))
	figure.legend(by_label.values(), by_label.keys(), fontsize=20)


def get_matplotlib_plot(fig_mpl, ax, data_for_plotting):
	plt_plotter = PltPlotter(fig_mpl, ax, data_for_plotting)
	plt_plotter()


def download_mpl(fig_mpl):
	# mpl save
	mpl_buffer = io.BytesIO()
	fig_mpl.savefig(mpl_buffer, format="pdf")
	today = datetime.today().strftime('%Y-%m-%d')
	st.download_button(
		label="StreamlitDownloadFunctions Matplotlib pdf",
		data=mpl_buffer.getvalue(),
		file_name="principal_schem" + today + ".pdf",
		mime="pdf",
	)


class PltPolygonPlotter:
	def __init__(self, fig, ax, data_for_plotting: DataForPlotting):
		self.fig = fig
		self.ax = ax
		self.ax.set_aspect('equal')
		self.ax.axis('off')
		self.data_for_plotting = data_for_plotting
		self.polygon_points_merge_control = data_for_plotting.polygon_points_merge_control
		self._df = self.polygon_points_merge_control.df_text.df_to_revit
		self.level_property = self.polygon_points_merge_control.get_level_property()
		self.legend_points = []
		self.fig.set_size_inches(self.__get_plot_dimension())
		self.font_size = 12
		self.arrow_size = 12
		self.linewidth = 2
		self.all_system_points = self.polygon_points_merge_control.system_property_points

	def __call__(self, *args, **kwargs):
		self._plot_polygons_plot()
		self.add_text_to_plot()

	def _plot_polygons_plot(self):
		color_filter_name = self.polygon_points_merge_control.layout_view_context_data.space_data_view.plot_layout.color_filter_name
		for idx, row in self._df.iterrows():
			self.ax.plot(
				row["px"], row["py"], color=self.__check_color(row), linewidth=self.linewidth,
				label=row[color_filter_name]
			)

	def __check_unique_color_filter_legend(self, row, color_filter_column: str):
		legend_label = []

		if row[color_filter_column] in legend_label:
			legend_unique_check = None
		else:
			legend_label.append(row[color_filter_column])
			legend_unique_check = row[color_filter_column]
		return legend_unique_check

	def __check_color(self, row: pd.Series) -> str:
		if self.polygon_points_merge_control.layout_view_context_data.color_view_checkbox:
			return row["color"]
		else:
			return "grey"

	def __get_plot_dimension(self):
		mpl_plot_const = 20
		width = self.polygon_points_merge_control.layout_view_context_data.plot_width
		height = self.polygon_points_merge_control.layout_view_context_data.plot_height
		width_out = width / mpl_plot_const if width / mpl_plot_const <= 200 else 200
		height_out = height / mpl_plot_const if height / mpl_plot_const <= 200 else 200
		return self.cm_to_inch(width_out), self.cm_to_inch(height_out)

	@staticmethod
	def cm_to_inch(value):
		return value / 2.54

	def add_text_to_plot(self):
		for idx_, row in self._df.iterrows():
			self.ax.text(
				x=row["pcx"],
				y=row["pcy"],
				s=row["text"].replace("<br>", "\n"),
				family="issocuper",
				style='italic', fontsize=self.font_size, horizontalalignment='center',
				verticalalignment='top'

			)


class PltPlotter(PltPolygonPlotter):

	def __init__(self, fig, ax, data_for_plotting: DataForPlotting):
		super().__init__(fig, ax, data_for_plotting)

	def __call__(self, *args, **kwargs):
		self.plot_start_end_system_lines()
		self.plot_vertical_side_plot_lines_to_system()
		self.add_offset_sum_flow()
		self.add_level_text()
		self.plot_add_text_to_equipment_point()

	def __text_check_position_polygon_flow(self) -> dict:
		if self.polygon_points_merge_control.layout_view_context_data.vertical_direction_list == "up":
			return dict(horizontalalignment='center', verticalalignment='top')
		elif self.polygon_points_merge_control.layout_view_context_data.vertical_direction_list == "down":
			return dict(horizontalalignment='center', verticalalignment='bottom')

	def __text_check_position_system_name(self, text) -> dict:
		if self.polygon_points_merge_control.layout_view_context_data.vertical_direction_list == "up":
			return dict(s=f" {text}\n", horizontalalignment='center', verticalalignment='bottom')
		elif self.polygon_points_merge_control.layout_view_context_data.vertical_direction_list == "down":
			return dict(s=f"\n {text}", horizontalalignment='center', verticalalignment='top')

	def __text_check_position_level_flow(self) -> dict:
		if self.polygon_points_merge_control.layout_view_context_data.horizontal_direction_list == "left":
			return dict(horizontalalignment='left', verticalalignment='bottom')
		elif self.polygon_points_merge_control.layout_view_context_data.horizontal_direction_list == "right":
			return dict(horizontalalignment='right', verticalalignment='bottom')

	@staticmethod
	def __text_check_position(
			base_point_x: float, base_point_y: float, px: float, py: float
	):
		"""check position for equipment text"""

		if base_point_x > px and base_point_y == py:
			return "left", "center"
		elif base_point_x < px and base_point_y == py:
			return "right", "center"
		elif base_point_x == px and base_point_y > py:
			return "center", "bottom"
		else:
			return "center", "top"

	def __check_unique_name(self, point):
		if point.system_name in self.legend_points:
			legend_unique_check = None
		else:
			self.legend_points.append(point.system_name)
			legend_unique_check = point.system_name
		return legend_unique_check

	def legend_without_duplicate_labels(self, ax):
		handles, labels = ax.get_legend_handles_labels()
		unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
		ax.legend(*zip(*unique))

	def plot_start_end_system_lines(self):
		# from polygons up or down

		for point in self.all_system_points:
			# add flow
			self.ax.text(x=point.x_start_points, y=point.y_start_points, s=f"L={str(point.system_flow)}",
			             family="issocuper",
			             style='italic', fontsize=self.font_size, **self.__text_check_position_polygon_flow()
			             )
			# add system name
			self.ax.text(x=point.x_end_points, y=point.y_end_points,
			             family="issocuper",
			             style='italic', fontsize=self.font_size,
			             **self.__text_check_position_system_name(point.system_name)
			             )
			# add line from polygons up or down start point
			self.ax.plot(
				(point.x_start_points, point.x_end_points),
				(point.y_start_points, point.y_end_points),
				color=point.color, label=self.__check_unique_name(point),
				marker='1', markevery=point.x_start_points,
				markersize=self.arrow_size,
				linewidth=self.linewidth
			)

			# add line from end point of vertical system line to offset point
			self.ax.plot(
				(point.x_end_points, point.offset_point_x),
				(point.y_end_points, point.offset_point_y),
				color=point.color,
				marker=">", markersize=self.arrow_size,
				linewidth=self.linewidth
			)

	def plot_vertical_side_plot_lines_to_system(self):
		# between levels
		for idx_, row in self.polygon_points_merge_control.add_color_df.iterrows():
			self.ax.plot(
				(row["Max_x"], row["Min_x"]),
				(row["Max_y"], row["Min_y"]),
				color=row.color,
				linewidth=self.linewidth
			)

	def __plot_horizontal_line_to_equipment(self, row):
		self.ax.plot(
			[row["base_point_x"], row["px"]],
			[row["base_point_y"], row["py"]],
			color=row["color"],
			linewidth=self.linewidth
		)

	def add_offset_sum_flow(self):
		# from polygons up or down

		df_1 = pd.DataFrame([prop.__dict__ for prop in self.all_system_points])
		df_1 = df_1.groupby(['offset_point_x', 'offset_point_y'])["system_flow"].sum().reset_index()
		for point in self.all_system_points:
			# add offset sum flow
			for idx, row in df_1.iterrows():
				if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
					self.ax.text(x=point.offset_point_x, y=point.offset_point_y,
					             s=f"{point.system_name} {point.level_value} L={round(row['system_flow'])}",
					             family="issocuper",
					             style='italic', fontsize=self.font_size, **self.__text_check_position_level_flow()
					             )

	def add_level_text(self):
		for prop in self.level_property:
			if prop.vertical_direction_list == "up":
				self.ax.text(x=prop.level_coord_x, y=prop.level_coord_y,
				             s=f"{str(prop.level_name)}",
				             family="issocuper",
				             style='italic', fontsize=self.font_size, horizontalalignment='right',
				             verticalalignment='bottom'
				             )

	def plot_add_text_to_equipment_point(self):
		for en, df in enumerate(self.data_for_plotting.location_point_list):  # levels iteration
			for idx_, row in df.iterrows():  # df row iteration
				# horizontal line to equipment
				self.__plot_horizontal_line_to_equipment(row)
				# equipment text and marker
				__text_check_position = self.__text_check_position(df["base_point_x"].iat[0], df["base_point_y"].iat[0],
				                                                   df["px"].iat[0], df["py"].iat[0])
				self.ax.text(
					x=df["base_point_x"].iat[0], y=df["base_point_y"].iat[0],
					# name=self.data_for_plotting.dynamic_widgets_view_context_data.legend_group[en],
					s=str(df["system_name"].values[0]) +
					  '\n '
					  +
					  str(df[self.polygon_points_merge_control.layout_view_context_data.level_column].values[0]) +
					  '\n' +
					  str(self.data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]),
					family="issocuper",
					style='italic',
					fontsize=self.font_size,
					horizontalalignment=__text_check_position[0],
					verticalalignment=__text_check_position[1]
				)

				self.ax.scatter(
					x=df["base_point_x"],
					y=df["base_point_y"],
					marker="x",
					s=500

				)
