import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from InsertTerminalsPandas.Geometry.GeometryLines import Line, offset_polygon
from typing import List, Tuple, Dict, Set
from library_hvac_app.list_custom_functions import *


class PlotTestLines:

	def __init__(self, polygon: Polygon, lines: List[Line] = None, points_coordinates: list = None) -> None:
		self.x, self.y = polygon.exterior.xy
		self.lines = to_list(lines)
		self.points_coordinates = to_list(points_coordinates)
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot()
		self.ax.plot(self.x, self.y)
		self.point_style = dict(s=500, c='red', marker="s", linewidth=0.5)

	def _plot_scatters(self):
		if self.points_coordinates:
			if (isinstance(self.points_coordinates[0], float)
					or isinstance(self.points_coordinates[0], int)
			):
				self.ax.scatter(self.points_coordinates[0], self.points_coordinates[1],
				                **self.point_style
				                )
			else:
				self.ax.scatter([x[0] for x in self.points_coordinates], [x[1] for x in self.points_coordinates],
				                **self.point_style)

	def _plot_line(self, line: Line):
		if line:
			self.ax.plot((line.StartPoint.X, line.EndPoint.X), (line.StartPoint.Y, line.EndPoint.Y), color='blue',
			             linewidth=3, solid_capstyle='round')

	def plot_lines(self):
		if self.lines:
			for line in self.lines:
				self._plot_line(line)
