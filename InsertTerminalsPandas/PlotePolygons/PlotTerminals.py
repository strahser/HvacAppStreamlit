import io
from matplotlib import pyplot as plt
from InsertTerminalsPandas.InputData.input import *
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing


class PlotTerminalsAndSpaces:
	"""static class for plotting points(terminals) and polygons(spaces). Config grid"""

	def __init__(self):
		self.geometry = None
		self.color = None
		self.dimension = None

	def default_data(self, dimension, color, geometry):
		if not dimension:
			self.dimension = 100
		if not color:
			self.color = "c"
		if not geometry:
			self.geometry = "o"

	@staticmethod
	def _plot_line(ax, ob, color='b'):
		x, y = ob.exterior.xy
		ax.plot(x, y, color=color, linewidth=1)

	@staticmethod
	def plot_scatters(ax, points_coordinates, dimension=100, color="c", geometry="o"):

		point_style = dict(s=dimension / 2, c=color, marker=geometry)
		if points_coordinates:
			if isinstance(points_coordinates[0], float) or isinstance(points_coordinates[0], int):
				ax.scatter(points_coordinates[0], points_coordinates[1], **point_style)
			else:
				ax.scatter([x[0] for x in points_coordinates], [x[1] for x in points_coordinates],
				           **point_style)

	@staticmethod
	def add_text_to_df_terminals_points_column(ax, points_, text_):
		if isinstance(points_[0], float) or isinstance(points_[0], int):
			ax.text(points_[0] + 500, points_[1] + 600, text_)
		else:
			[ax.text(p_[0] + 500, p_[1], text_) for p_ in points_]

	@staticmethod
	def plot_terminals(ax, level_df_data: pd.DataFrame, system_type: str, input_data_df: InputDataDF):
		"""plot points from df

        Args:
            system_type ():
            input_data_df ():
            ax (matplotlib): ax of matplotlib
            level_df_data (pd.DataFrame): AddCalculatedPointsToDF
        """
		sys_dict = input_data_df.system_dictionary
		for index, row in level_df_data.iterrows():
			PlotTerminalsAndSpaces.plot_scatters(ax, row.points, row.dimension1, row.color, row.geometry)
			PlotTerminalsAndSpaces.add_text_to_df_terminals_points_column(ax, row.points, row[sys_dict[system_type].system_name])

	@staticmethod
	def plot_offset_spaces(ax, level_df_data: pd.DataFrame):
		for index, row in level_df_data.iterrows():
			PlotTerminalsAndSpaces._plot_line(ax, row.offset_polygon, "grey")

	def add_grid(ax):
		ax.grid(which='major', color='k', linewidth=1)

		# Defining the appearance of the auxiliary grid lines:
		ax.grid(which='minor',
		        color='k',
		        linestyle=':')

	@staticmethod
	def plot_spaces(ax, all_level_spaces: pd.DataFrame, text_columns=None):

		if text_columns is None:
			text_columns = [ColumnChoosing.S_ID, ColumnChoosing.S_Name]
		all_level_spaces = all_level_spaces.copy()
		all_level_spaces['add_text'] = all_level_spaces[text_columns].astype(str).agg('\n'.join, axis=1)
		for index, row in all_level_spaces.iterrows():
			PlotTerminalsAndSpaces._plot_line(ax, row.polygon, "grey")
			ax.text(row.pcx, row.pcy, row.add_text)

	@staticmethod
	def save_plot(fig):
		img = io.StringIO()
		plt.axis('off')
		fig.savefig(img, format='svg')
		# clip off the xml headers from the image
		svg_img = '<svg' + img.getvalue().split('<svg')[1]
		return svg_img
