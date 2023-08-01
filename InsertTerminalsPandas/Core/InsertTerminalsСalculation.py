from InsertTerminalsPandas.Geometry.GeometryLines import *
from InsertTerminalsPandas.Geometry.GeometryTerminals import *


class InsertTerminals:
	def __init__(self,
	             perimeter_curve: Line,
	             device_orientation_option1: str,
	             device_orientation_option2: str,
	             location_type: str,
	             device_points_number: int | float
	             ):
		self.perimeter_curve = perimeter_curve
		self.device_orientation_option1 = device_orientation_option1
		self.device_orientation_option2 = device_orientation_option2
		self.location_type = location_type
		self.device_points_number = device_points_number

	def _create_curve_filter(self):
		curve_dict = CreateCurveDictionary(self.perimeter_curve)
		curve_dict._get_curves_location()
		curve_dictionary = curve_dict.get_filter_curve_dict()
		curve_filter = CreateCurvesFilters(
			curve_dictionary,
			self.device_orientation_option1,
			self.device_orientation_option2,
			self.location_type,
			self.device_points_number,
			True
		)
		return curve_filter

	def get_long_curve_length(self):
		curve_filter = self._create_curve_filter()
		curve_filter._choose_long_short_curve_filter()
		return curve_filter.long_curve.Length

	def insert_terminals_in_space(self):
		curve_filter = self._create_curve_filter()
		points = curve_filter.split_curve_by_point_definition()
		return points
