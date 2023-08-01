import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
polygons = os.path.join(parent_dir, "Polygons")
library = os.path.join(parent_dir, "library_hvac_app")
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
sys.path.insert(0, polygons)
sys.path.insert(0, library)
from PloteNetworksAndSpaces.PrincipalSchems.Models.ModelsUpdate import *
from linque import Linque

# region input

input_df_path = os.path.abspath(os.path.join(parent_dir, "to_revit_init.xlsx"))
input_df = pd.read_excel(input_df_path, sheet_name="revit_export")
system_column = 'ПритНаим'
system_flow_column = "ПритВозМакс"
s_level = "УровеньПом"
s_id = "S_ID"
vertical_direction = "up"
horizontal_direction = "left"
system_property_type = "system_property_list1"
cond = input_df[s_level] == "Этаж 01"
# endregion

filter_df = input_df[cond]
list_of_id = filter_df[s_id].tolist()
# test 1 PolygonsCreatorModel
polygon_coordinates = PolygonCoordinates()
polygon_creator_model = PolygonsCreatorModel(list_of_id, polygon_coordinates)
space_property_list = polygon_creator_model.get_polygon_property()
print(space_property_list)

system_property_list: list[SystemProperty] = []
# add id,system_name,system_flow,level,
# system_property_type(1 or 2?) id,system_column,system_flow_column
for idx_, row in filter_df.iterrows():
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
lq_system_property_list = Linque(system_property_list)
lq_space_property_list = Linque(space_property_list)
print(lq_system_property_list.where(lambda x: x.system_flow == 0)
      .select(lambda x: x.system_flow)
      .to_list())


def get_vertical_direction(space_property: SpaceProperty) -> str:
	vertical_direction = Linque(space_property.system_property_list1). \
		where(lambda x: x.vertical_direction). \
		select(lambda x: x.vertical_direction). \
		first()
	return vertical_direction


def choose_system_property_by_system_property_type(
		system_property_list: list[SystemProperty],
		space_property: SpaceProperty,
		system_property_type: str) -> list[SystemProperty]:
	return Linque(system_property_list). \
		where(lambda x: x.space_id == space_property.space_id
	                    and x.system_property_type == system_property_type).to_list()


for space_property in space_property_list:
	setattr(space_property, system_property_type,
	        choose_system_property_by_system_property_type(
		        system_property_list,
		        space_property,
		        system_property_type)
	        )
	polygon_points_coordinates = space_property.curve_dictionary[get_vertical_direction(space_property)]. \
		_get_standard_points(len(space_property.system_property_list1))
	space_property.polygon_points_list1 = polygon_points_coordinates
	for points, systems in zip(polygon_points_coordinates, space_property.system_property_list1):
		systems.x_start_points = points[0]
		systems.y_start_points = points[1]

print(space_property_list)
