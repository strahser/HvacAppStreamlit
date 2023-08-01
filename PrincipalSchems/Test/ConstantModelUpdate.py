from shapely.geometry import Polygon
from dataclasses import dataclass


@dataclass()
class SystemProperty:
	space_id: str = None
	system_name: str = None
	system_flow: float = None
	level_value: str = None
	vertical_direction: str = None
	horizontal_direction: str = None
	distance_to_line: int = 20
	color: str = None
	x_start_points: float = 0
	y_start_points: float = 0
	x_end_points: float = 0
	y_end_points: float = 0
	offset_point_x: float = 0
	offset_point_y: float = 0
	system_property_type: str = None


@dataclass()
class SpaceProperty:
	space_id: str = None
	level_value: str = None
	px: float = None
	py: float = None
	pcx: float = None
	pcy: float = None
	system_property_list1: list[SystemProperty] = None
	system_property_list2: list[SystemProperty] = None
	polygon_points_list1:list[float] = None
	polygon_points_list2: list[float] = None
	polygon: Polygon = None
	curve_dictionary:dict =None


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
