from InsertTerminalsPandas.Models.DeviceModel import *
from InsertTerminalsPandas.Core.InsertTerminalsСalculation import *
from InsertTerminalsPandas.Core.ChooseTerminalFromDBModel import *
from InsertTerminalsPandas.PlotePolygons.PlotTerminals import *
from InsertTerminalsPandas.TermilalView.DevicePropertyView import DevicePropertyView
import streamlit as st


class BaseDictDB:
	def __init__(self, dictionary_parsing: dict):
		for k, v in dictionary_parsing.items():
			setattr(self, k, v)


class TerminalDB(BaseDictDB):
	def __init__(self, dictionary_parsing: dict):
		super().__init__(dictionary_parsing)


class SelectedTerminalCalculation:
	
	@staticmethod
	def __check_short_line_points(device_layout: DevicePropertyView,
	                              short_line: Line,
	                              minimum_device_number: int):
		if short_line.Length >= device_layout.directive_length:
			line_points = math.ceil(short_line.Length / device_layout.directive_length)
			short_line_points = line_points if line_points >= minimum_device_number else minimum_device_number
			return short_line_points
	
	def _checking_calculation_option(self,
	                                 device_layout: DevicePropertyView,
	                                 polygon_dict_record: dict,
	                                 minimum_device_number: int
	                                 ):
		"""
		Args:
			device_layout:
			polygon_dict_record: Polygon  DF to dict
			minimum_device_number:
		Returns:
		"""
		if device_layout.calculation_options == "device_area":
			points_number = math.ceil(polygon_dict_record[ColumnChoosing.S_area] / device_layout.device_area)
			return minimum_device_number if minimum_device_number >= points_number else points_number
		
		if device_layout.calculation_options == "directive_length":
			polygon_lines = polygon_dict_record["polygon"].exterior.coords
			perimeter_curve_dictionary = CreateCurveDictionary(gl.GeometryUtility.get_lines_in_polygon(polygon_lines))
			short_line, long_line = CreateCurveDictionary.choose_long_short_curve_filter(
				perimeter_curve_dictionary.get_filter_curve_dict(),
				device_layout.device_orientation_option1,
				device_layout.device_orientation_option2
			)
			short_line_points = self.__check_short_line_points(device_layout, short_line, minimum_device_number)
			long_line_points = self.__check_short_line_points(device_layout, long_line, minimum_device_number)
			return short_line_points if short_line_points <= 2 else long_line_points
		
		if device_layout.calculation_options == "directive_terminals":
			return device_layout.directive_terminals if device_layout.directive_terminals > minimum_device_number else\
				minimum_device_number
	
	def choose_terminal_from_calculation_option(self, device_layout: DevicePropertyView,
	                                            polygon_dict_record: dict,
	                                            choosing_terminal: ChooseTerminalsInstanceFromDB
	                                            
	                                            ):
		
		choosing_terminal_data = choosing_terminal.get_minimum_device_number().to_dict("records")[0]
		if device_layout.calculation_options == 'minimum_terminals':
			return TerminalDB(choosing_terminal_data)
		else:
			points_number = self._checking_calculation_option(device_layout,
			                                                  polygon_dict_record,
			                                                  choosing_terminal_data["minimum_device_number"]
			                                                  )
			choosing_terminal_data_from_point_number = choosing_terminal. \
				get_terminal_from_points_number(points_number).to_dict("records")[0]
			return TerminalDB(choosing_terminal_data_from_point_number)


class ParsingDBtoTerminalDataControl:
	def __init__(self, df_polygons, config_layout, input_data_df):
		self.df_polygons = df_polygons
		self.config_layout = config_layout
		self.input_data_df = input_data_df
	
	@staticmethod
	def _populate_attributes(class_data_input, class_data_populate, name_of_data_populate_attr):
		if hasattr(class_data_input, name_of_data_populate_attr):
			class_data_input_populate_att = getattr(class_data_input, name_of_data_populate_attr)
			setattr(class_data_populate, name_of_data_populate_attr, class_data_input_populate_att)
			return class_data_populate
	
	def _add_device_layout(self, system_):
		st.subheader(f"Detail Config of  {system_.replace('_', ' ').title()}")
		with st.expander(''):
			self.device_layout = DevicePropertyView(system_, self.input_data_df)
			self.device_layout.get_terminal_layout()
		return self.device_layout
	
	def add_parsing_data_to_device_model(self, system_color_dictionary: dict, selected_id: list[int | str]):
		string_id_list = [str(val) for val in selected_id]
		condition = self.df_polygons[ColumnChoosing.S_ID].isin(string_id_list)
		device_property_list = []
		self.device_layout_list = []
		polygon_df_dictionary: dict = self.df_polygons.to_dict("records")
		if any(condition):
			for system_ in self.config_layout.system_select:
				device_layout = self._add_device_layout(system_)
				self.device_layout_list.append(device_layout)
				system_flow_column = self.input_data_df.system_dictionary[system_].system_flow
				system_name_column = self.input_data_df.system_dictionary[system_].system_name
				system_id_column = ColumnChoosing.S_ID
				for polygon_dict_record in polygon_df_dictionary:
					device_property = Device()
					for name in device_property.__annotations__:
						self._populate_attributes(device_layout, device_property, name)
					device_property.system_name = polygon_dict_record[system_name_column]
					device_property.space_id = polygon_dict_record[system_id_column]
					device_property.space_flow = polygon_dict_record[system_flow_column]
					family_device_name = getattr(device_property, ColumnChoosing.family_device_name)
					choosing_terminal = ChooseTerminalsInstanceFromDB(
						self.input_data_df.concat_base,
						family_device_name,
						polygon_dict_record[system_flow_column]
					)
					if device_property.space_flow:
						selected_terminal_calculation = SelectedTerminalCalculation()
						terminal_db = selected_terminal_calculation.choose_terminal_from_calculation_option(
							device_layout,
							polygon_dict_record,
							choosing_terminal
						)
						for name in device_property.__annotations__:
							self._populate_attributes(terminal_db, device_property, name)
						device_property.calculate_device_flow_and_k_ef()
						try:
							offset_polygon = polygon_dict_record["polygon"].buffer(-device_property.wall_offset,
							                                                       join_style=2)
							perimeter_curve = gl.GeometryUtility.get_lines_in_polygon(offset_polygon.exterior.coords)

							terminals = InsertTerminals(perimeter_curve,
							                            device_property.device_orientation_option1,
							                            device_property.device_orientation_option2,
							                            device_property.single_device_orientation,
							                            device_property.minimum_device_number
							                            )

							device_property.point_x_y_list = terminals.insert_terminals_in_space()
							device_property.point_z = polygon_dict_record["pz"][0] - device_property.ceiling_offset
							device_property.color = system_color_dictionary[device_property.system_name]
							device_property_list.append(device_property)
						except Exception as e:
							st.warning(
								f" cannot make system __{device_property.system_name}__ in  __{polygon_dict_record[system_id_column]}__ \n error like {e}")
		return device_property_list


class PlotSelectedSpacesAndTerminals:
	
	@staticmethod
	def plot_selected_terminals(ax, device_property):
		PlotTerminalsAndSpaces.plot_scatters(ax, device_property.point_x_y_list,
		                                     device_property.dimension1 / 2,
		                                     device_property.color, device_property.geometry)
		PlotTerminalsAndSpaces.add_text_to_df_terminals_points_column(ax,
		                                                              device_property.point_x_y_list,
		                                                              device_property.system_name)
	
	@staticmethod
	def plot_selected_polygons(df_polygons, ax, selected_id: list[int | str]):
		string_id_list = [str(val) for val in selected_id]
		condition = df_polygons[ColumnChoosing.S_ID].isin(string_id_list)
		if any(condition):
			PlotTerminalsAndSpaces.plot_spaces(ax, df_polygons[condition])
		else:
			PlotTerminalsAndSpaces.plot_spaces(ax, df_polygons)
		return string_id_list
