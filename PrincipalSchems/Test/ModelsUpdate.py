# region Model
import pandas as pd
from linque import Linque
from PrincipalSchems.Geometry import CreateCurvesFromStartPoint, gl
from PrincipalSchems.Models.ConstantModel import *


class SpacePropertyCreatorModel:
	def __init__(self, list_of_id: list[str], polygon_coordinates: PolygonCoordinates):
		"""create polygon with property """

		self.min_x_polygon = None
		self.max_x_polygon = None
		self.list_of_id = list_of_id
		self.start_x = polygon_coordinates.start_x
		self.start_y = polygon_coordinates.start_y
		self.step_x = polygon_coordinates.step_x
		self.step_y = polygon_coordinates.step_y

	def create_polygons(self) -> list[SpaceProperty]:
		"""create polygons with offset in right direction on axis X. add id"""
		polygon_property_list = []
		start_x = self.start_x
		for id_ in self.list_of_id:
			space_property = SpaceProperty()
			polygon = Polygon(
				[
					(start_x, self.start_y),
					(start_x, self.start_y + self.step_y),
					(start_x + self.step_x, self.start_y + self.step_y),
					(start_x + self.step_x, self.start_y),
				]
			)
			start_x += self.step_x
			space_property.space_id = id_
			space_property.polygon = polygon
			polygon_property_list.append(space_property)

		return polygon_property_list

	def get_curve_dictionary(self, polygon):
		space_perimetr = gl.GeometryUtility.get_lines_in_polygon(
			polygon.exterior.coords
		)
		curve_dict = CreateCurvesFromStartPoint(space_perimetr)
		curve_dict._get_curves_location()
		curve_dictionary = curve_dict.get_filter_curve_dict()
		return curve_dictionary

	def create_space_property(
			self, x_max_calculate: int = None
	) -> list[SpaceProperty]:
		"""add to space_property_list px,py,pcx,pcy,x_min,x_max:"""
		space_property_list = self.create_polygons()
		space_property_list_add_values = []

		for space_property in space_property_list:
			px, py = space_property.polygon.exterior.xy
			space_property.px = list(px)
			space_property.py = list(py)
			space_property.pcx = list(space_property.polygon.centroid.coords.xy[0])[0]
			space_property.pcy = list(space_property.polygon.centroid.coords.xy[1])[0]
			space_property_list_add_values.append(space_property)
			space_property.curve_dictionary = self.get_curve_dictionary(space_property.polygon)

		if x_max_calculate:
			self.max_x_polygon = x_max_calculate
		else:
			self.max_x_polygon = max([space_property.px for space_property in space_property_list_add_values])
		self.min_x_polygon = min([space_property.px for space_property in space_property_list_add_values])
		return space_property_list_add_values


class SystemPropertyModel:
	def __init__(self, filter_df: pd.DataFrame):
		self.filter_df = filter_df

	def add_data_to_system_property(self,
	                                s_id: str,
	                                s_level: str,
	                                system_column: str,
	                                system_flow_column: float,
	                                vertical_direction: str,
	                                horizontal_direction: str,
	                                system_property_type: str
	                                ) -> list[SystemProperty]:
		system_property_list = []
		for idx_, row in self.filter_df.iterrows():
			system_property = SystemProperty()
			if row[system_column]:
				system_property.space_id = row[s_id]
				system_property.system_name = row[system_column]
				system_property.system_flow = row[system_flow_column]
				system_property.level_value = row[s_level]
				system_property.vertical_direction = vertical_direction
				system_property.horizontal_direction = horizontal_direction
				system_property.system_property_type = system_property_type
			system_property_list.append(system_property)

class MergeSystemPropertyToSpaceProperty:
	def __init__(self, system_property_type: str, system_property_list: list[SystemProperty]):
		self.system_property_type = system_property_type
		self.system_property_list = system_property_list

	def _get_vertical_direction_name(self, space_property: SpaceProperty) -> str:
		vertical_direction = Linque(getattr(space_property, self.system_property_type)). \
			where(lambda x: x.vertical_direction). \
			select(lambda x: x.vertical_direction). \
			first()
		return vertical_direction

	def _choose_system_property_by_system_property_type(self, space_property: SpaceProperty) -> list[SystemProperty]:
		return Linque(self.system_property_list). \
			where(lambda x: x.space_id == space_property.space_id
		                    and x.system_property_type == self.system_property_type).to_list()

	# def add_data_to_polygon_points_list(self) -> list[SystemProperty]:
	# 	for space_property in self.system_property_list:
	# 		number_of_systems = len(space_property.system_property_list1
	# 		setattr(space_property, self.system_property_type,
	# 		        self._choose_system_property_by_system_property_type(space_property)
	# 		        )
	# 		polygon_points_coordinates = space_property.curve_dictionary[
	# 			self._get_vertical_direction_name(space_property)]. \
	# 			_get_standard_points(number_of_systems)
	# 		                         )
	# 		space_property.polygon_points_list1 = polygon_points_coordinates

# class SystemPropertyStartPointsModel:
# 	def __init__(self, system_property_type: str, system_property_list: list[SystemProperty]):
# 		self.system_property_type = system_property_type
# 		self.system_property_list = system_property_list
#
# 	def _get_vertical_direction_name(self, space_property: SpaceProperty) -> str:
# 		vertical_direction = Linque(getattr(space_property, self.system_property_type)). \
# 			where(lambda x: x.vertical_direction). \
# 			select(lambda x: x.vertical_direction). \
# 			first()
# 		return vertical_direction
#
# 	def _choose_system_property_by_system_property_type(self, space_property: SpaceProperty) -> list[SystemProperty]:
#
# 		return Linque(self.system_property_list). \
# 			where(lambda x: x.space_id == space_property.space_id
# 		                    and x.system_property_type == self.system_property_type).to_list()
#
# 	def set_start_points_system_coordinates(self) -> list[SystemProperty]:
# 		for space_property in self.system_property_list:
# 			number_of_systems = len(space_property.system_property_list1
# 			setattr(space_property, self.system_property_type,
# 			        self._choose_system_property_by_system_property_type(space_property)
# 			        )
# 			polygon_points_coordinates = space_property.curve_dictionary[
# 				self._get_vertical_direction_name(space_property)]. \
# 				_get_standard_points(number_of_systems)
# 			                         )
# 			space_property.polygon_points_list1 = polygon_points_coordinates
# 			for points, systems in zip(polygon_points_coordinates, space_property.system_property_list1):
# 				systems.x_start_points = points[0]
# 				systems.y_start_points = points[1]
# 		return space_property_list


class SystemPropertyEndPointsModel:
	def __init__(
			self, line_direction: str = "up", system_direction: str = "right"
	) -> None:
		self.line_direction = line_direction
		self.system_direction = system_direction

	def check_line_direction(
			self,
			system_property: SystemProperty,
			max_polygon_coord_x: int,
			min_polygon_coord_x: int,
			offset: int = 0,
	) -> SystemProperty:
		"""create filter on up/down and right/left direction

        Args:
            y_start_point (int): _description_
            system_property (SystemProperty): _description_
            key (str): system name
            max_polygon_coord_x (int): max or min coordinate of polygon
            offset (int): system line offset

        Returns:
            SystemProperty: add x, y end points, offset points
        """
		if self.line_direction == "up" and self.system_direction == "right":
			system_property.y_end_points = (
					system_property.y_start_points + system_property.distance_to_line
			)
			offset_point_x = (
					max_polygon_coord_x + offset + system_property.distance_to_line
			)

		elif self.line_direction == "up" and self.system_direction == "left":
			system_property.y_end_points = (
					system_property.y_start_points + system_property.distance_to_line
			)
			offset_point_x = (
					min_polygon_coord_x - offset - system_property.distance_to_line
			)

		elif self.line_direction == "down" and self.system_direction == "right":
			system_property.y_end_points = (
					system_property.y_start_points - system_property.distance_to_line
			)
			offset_point_x = (
					max_polygon_coord_x + offset + system_property.distance_to_line
			)

		elif self.line_direction == "down" and self.system_direction == "left":
			system_property.y_end_points = (
					system_property.y_start_points - system_property.distance_to_line
			)
			offset_point_x = (
					min_polygon_coord_x - offset - system_property.distance_to_line
			)
		system_property.x_end_points = system_property.x_start_points
		system_property.offset_point_x = offset_point_x
		system_property.offset_point_y = system_property.y_end_points
		return system_property


# class PolygonMainModel:
# 	def __init__(
# 			self,
# 			df_dict: Dict[str, list[str]],
# 			start_y: int = 0,
# 			max_space_count: float = 0,
# 			step_x: int = 50,
# 			step_y: int = 50,
# 	) -> None:
# 		"""calculate start and end points
#         """
#
# 		self.polygon_coordinates = PolygonCoordinates(
# 			start_y=start_y, step_x=step_x, step_y=step_y
# 		)
# 		self.polygon_creator = PolygonsCreatorModel(
# 			df_dict.keys(), self.polygon_coordinates
# 		)
# 		self.polygon_dict = self.polygon_creator.create_polygons()
# 		self.x_max_calculate = max_space_count * self.polygon_creator.step_x
# 		self.polygon_property = self.polygon_creator.get_polygon_property(
# 			self.x_max_calculate
# 		)
#
#
# class PointsMainModel:
# 	def __init__(self, df_property, polygon_main_model: PolygonMainModel):
# 		"""calculate start and end points
#
#         Args:
#             df_dict (SystemGroupCreator.create_dictionary_from_df): _description_
#             df_property (_type_): _description_
#             start_y (int, optional): _description_. Defaults to 0.
#             max_space_count (float, optional): for calculation max spaces. Defaults to None.
#             step_x (int, optional): _description_. Defaults to 50.
#             step_y (int, optional): _description_. Defaults to 50.
#         """
# 		self.df_property = df_property
# 		self.polygon_main_model = polygon_main_model
#
# 	def get_system_points(
# 			self, line_direction: str, system_direction: str
# 	) -> list[SystemProperty]:
# 		"""add SystemProperty start end point from filter of SchemeFilterModel"""
# 		all_points = []
# 		# in dict id:Polygons
# 		for key in self.polygon_main_model.polygon_dict.keys():
# 			filter_val = [val for val in self.df_property if val.space_id == key]
# 			start_points = StartPointsModel.get_start_line_points(
# 				line_direction, self.polygon_main_model.polygon_dict[key], filter_val
# 			)
# 			# in list of SystemProperty
# 			for point_ in start_points:
# 				scheme_filter = FilterEndPointsModel(line_direction, system_direction)
# 				scheme_filter_points = scheme_filter.check_line_direction(
# 					point_,
# 					self.polygon_main_model.polygon_creator.max_x_polygon,
# 					self.polygon_main_model.polygon_creator.min_x_polygon,
# 				)
# 				all_points.append(scheme_filter_points)
# 		return all_points
#

class SystemLocationModelBase:
	def __init__(
			self,
			system_property_points: list[SystemProperty],
			input_df: pd.DataFrame,
			system_name: str,
			level_name: str,
			level_column: str,
	) -> None:
		"""define equipment point"""
		self.system_property_points = system_property_points
		self.input_df = input_df
		self.system_name = system_name
		self.level_name = level_name
		self.level_column = level_column

	def _create_filter_base_property(self) -> list[SystemProperty]:
		filtered_points = [
			p for p in self.system_property_points if p.system_name == self.system_name
		]
		return filtered_points

	def _get_single_system_property(self) -> SystemProperty:
		filtered_points = self._create_filter_base_property()
		return filtered_points[0] if filtered_points else None

	def _create_filter_system_property(self) -> list[(str, str, str, float, float)]:
		filtered_points = [
			(p.space_id, p.system_name, p.color, p.offset_point_x, p.offset_point_y)
			for p in self._create_filter_base_property()
		]
		return filtered_points

	def create_filtered_df(self) -> pd.DataFrame:
		filtered_points = self._create_filter_system_property()
		return pd.DataFrame(
			columns=["S_ID", "system_name", "color", "px", "py"],
			data=filtered_points,
		)

	def merge_filtered_df_with_init_df(self) -> pd.DataFrame:
		df = self.create_filtered_df()
		return df.merge(self.input_df, on="S_ID", how="left")

	def create_model_unique_level(self) -> pd.DataFrame:
		return self.merge_filtered_df_with_init_df()[self.level_column].unique()

	def _is_equipment_level_in_system_level(self) -> bool:
		return self.level_name in self.create_model_unique_level()

	@staticmethod
	def cumsum(n_count: int, dist: float) -> list[int]:
		"""make list wit cumsum. Start distance add to value count

        Args:
            n_count (int): value count
            dist (float): Start distance

        Returns:
            list: list of cumsum
        """
		counter = 0
		temp_list = []
		for i in range(n_count):
			temp_list.append(counter)
			counter += dist
		return temp_list

	@staticmethod
	def create_system_base_point(
			direction: str, equipment_horizontal, start_point_x, start_point_y
	) -> list[float, float]:

		if direction == "left":
			base_point_x = start_point_x - equipment_horizontal
		else:
			base_point_x = start_point_x + equipment_horizontal
		return base_point_x, start_point_y


class ExistLevelLocationModel:
	def __init__(self, system_location_model: SystemLocationModelBase) -> pd.DataFrame:
		self.system_location_model = system_location_model
		self.level_column = system_location_model.level_column
		self.level_name = system_location_model.level_name

	def create_level_filter_model(self) -> pd.DataFrame:
		model_unique_level = self.system_location_model.merge_filtered_df_with_init_df()
		query_ = model_unique_level[self.level_column] == self.level_name
		model_unique_level = model_unique_level[query_]
		return model_unique_level

	def create_exist_level_equipment_base_point(
			self, system_direction: str, equipment_horizontal: float
	) -> pd.DataFrame:
		"""return equipment base point.Equipment point"""
		model_unique_level = self.create_level_filter_model()
		model_unique_level["base_point_x"] = model_unique_level.apply(
			lambda df: SystemLocationModelBase.create_system_base_point(
				system_direction,
				equipment_horizontal,
				df["px"],
				df["py"],
			)[0],
			axis=1,
		)
		model_unique_level["base_point_y"] = model_unique_level.apply(
			lambda df: SystemLocationModelBase.create_system_base_point(
				system_direction,
				equipment_horizontal,
				df["px"],
				df["py"],
			)[1],
			axis=1,
		)
		return model_unique_level


class NewLevelLocationModel:
	def __init__(self, system_location_model: SystemLocationModelBase) -> None:
		self.system_location_model = system_location_model
		self.level_column = system_location_model.level_column
		self.level_name = system_location_model.level_name

	def create_all_level_coordinates(self, level_dist: float) -> pd.DataFrame:
		unique_levels = self.system_location_model.input_df[self.level_column].unique()
		filter_input_df = pd.DataFrame({self.level_column: unique_levels})
		level_range = SystemLocationModelBase.cumsum(len(unique_levels), level_dist)
		filter_input_df["base_point_y"] = level_range
		return filter_input_df

	def create_new_filter_level_coordinate(self, level_dist: float) -> pd.DataFrame:
		new_coordinate_df = self.create_all_level_coordinates(level_dist)
		query_ = new_coordinate_df[self.level_column] == self.level_name
		new_coordinate_df = new_coordinate_df[query_]

		return new_coordinate_df

	def create_equipment_location(self, level_dist) -> EquipmentLocation:
		single_system_property = (
			self.system_location_model._get_single_system_property()
		)

		new_coordinate_df = self.create_new_filter_level_coordinate(level_dist)
		equipment_location = EquipmentLocation()
		attributes = [
			"base_point_x",
			"base_point_y",
			"px",
			"py",
			"color",
			"system_name",
			self.level_column,
		]
		data = [
			single_system_property.offset_point_x,
			new_coordinate_df["base_point_y"].values[0],
			single_system_property.offset_point_x,
			single_system_property.offset_point_y,
			single_system_property.color,
			single_system_property.system_name,
			new_coordinate_df[self.level_column].values[0],
		]
		for attr, val in zip(attributes, data):
			setattr(equipment_location, attr, val)
		return equipment_location

	def add_create_equipment_location_to_df(self, level_dist) -> pd.DataFrame:
		equipment_location = self.create_equipment_location(level_dist)
		columns = [
			"base_point_x",
			"base_point_y",
			"px",
			"py",
			"color",
			"system_name",
			self.level_column,
		]
		data = [[getattr(equipment_location, col)] for col in columns]
		data_dict = dict(zip(columns, data))
		new_coordinate_df = pd.DataFrame(data_dict)
		return new_coordinate_df

# endregion
