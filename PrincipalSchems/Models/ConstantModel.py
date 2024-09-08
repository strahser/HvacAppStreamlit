import math

from shapely.geometry import Polygon
from dataclasses import dataclass, field


@dataclass
class SystemProperty:
	space_id: str = None
	system_name: str = None
	system_flow: float = None
	level_value: float = None
	vertical_direction_list: float = None
	horizontal_direction_list: float = None
	distance_to_line: float = None
	color: str = None
	x_start_points: float = None
	y_start_points: float = None
	x_end_points: float = None
	y_end_points: float = None
	offset_point_x: float = None
	offset_point_y: float = None
	level_distance: float  = None

	def calculate_distance(self):
		try:
			return math.sqrt(
				(self.offset_point_x - self.x_end_points) ** 2 + (self.offset_point_y - self.y_end_points) ** 2)
		except Exception as e:
			print(e)
			return    0


class Space:
	def __init__(self):
		self.space_id = None
		self.level_value = None
		self.system_property_list: list[SystemProperty] = None
		self.polygon_list: list[Polygon]


class LevelPropertyModel:
	def __init__(self) -> None:
		self.level_name: str = None
		self.system_y: float = None
		self.level_coord_x: float = None
		self.level_coord_y: float = None
		self.vertical_direction_list: str = None


class Equipment:
	def __init__(self) -> None:
		self.system_name = None
		self.flow = None
		self.location_point: EquipmentLocation = None


class PolygonCoordinates:
	"""static structure"""

	def __init__(self, start_x=0, start_y=0, step_x=20, step_y=20) -> None:
		self.start_x = start_x
		self.start_y = start_y
		self.step_x = step_x
		self.step_y = step_y


class EquipmentLocation:
	def __init__(self) -> None:
		self.level = None
		self.base_point_y = None
		self.base_point_x = None
		self.px = None
		self.py = None
		self.color = None
		self.system_name = None
