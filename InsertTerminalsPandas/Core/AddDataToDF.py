from InsertTerminalsPandas.Core.InsertTerminalsСalculation import InsertTerminals, Polygon, gl
from InsertTerminalsPandas.Core.UpdateDFModel import DataFrameUpdating
from InsertTerminalsPandas.Core.ChooseTerminalFromDBModel import ChooseTerminalsInstanceFromDB, math
from InsertTerminalsPandas.PlotePolygons.PolygonMerge import PolygonMergeBase, PolygonMerge
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
from InsertTerminalsPandas.Core.JoinDFModel import JoinRevitExportTerminalsSheets, pd, InputDataDF
from StaticData.Exception import *


class FilterEmptySpaceTerminalsInDF:
	def __init__(self, system_type: str, input_data_df: InputDataDF):
		"""join spaces and device property's(Excel sheets devices,device_type and revit_export) and filtered
            empty family_device_name and system_flow

        Args:
             system_type (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
		self.system_type = system_type
		self.input_data_df = input_data_df
		self.system_flow = input_data_df.system_dictionary[system_type].system_flow

	def _get_join_spaces_and_devices(self, df_: pd.DataFrame) -> pd.DataFrame:
		joined_table = JoinRevitExportTerminalsSheets(self.system_type, self.input_data_df)
		space_and_terminal = joined_table.join_spaces_and_devices(df_)
		return space_and_terminal

	def _make_filter_notnull_system_flow(self, df_: pd.DataFrame) -> pd.DataFrame:
		df_ = df_[df_[self.system_flow].notnull()]
		return df_

	def _make_filter_notnull_family_device_name(self, df_) -> pd.DataFrame:
		df_ = df_[df_[ColumnChoosing.family_device_name].notnull()]
		return df_

	def make_filter_spaces_and_terminals_notnull(self, df_: pd.DataFrame) -> pd.DataFrame:
		space_and_terminal = self._get_join_spaces_and_devices(df_)
		space_and_terminal = self._make_filter_notnull_system_flow(space_and_terminal)
		space_and_terminal = self._make_filter_notnull_family_device_name(space_and_terminal)
		return space_and_terminal


class CalculateSpaceTerminalsInDF:
	def __init__(self, space_and_terminal: pd.DataFrame, system_type: str, input_data_df):
		"""apply ChooseTerminalsInstanceFromDB to FilterEmptySpaceTerminalsInDF

        Args:
            space_and_terminal (FilterEmptySpaceTerminalsInDF): _description_

        Returns:
            pd.DataFrame: _description_
        """
		self.space_and_terminal = space_and_terminal
		self.system_flow = input_data_df.system_dictionary[system_type].system_flow
		self.input_data_df = input_data_df

	def _calculation_factory(self) -> pd.DataFrame:
		"""make general loop from calculation_option in option_df
        Returns:
            pd.DataFrame: terminal choosing instance.
        """
		terminal_base = []
		for index, row in self.space_and_terminal.iterrows():
			option_df = self._checking_calculation_option(row)
			temp = option_df.assign(S_ID=row[ColumnChoosing.S_ID])
			terminal_base.append(temp)
		terminal_base_concat = pd.concat(terminal_base) \
			.reset_index(drop=True) \
			.drop(ColumnChoosing.family_device_name, axis=1)
		return terminal_base_concat

	def _checking_calculation_option(self, row):
		choosing_terminal = ChooseTerminalsInstanceFromDB(
			self.input_data_df.concat_base,
			row[ColumnChoosing.family_device_name],
			row[self.system_flow],
		)

		if row['directive_terminals']:
			res = choosing_terminal.get_terminal_from_points_number(row['directive_terminals'])
			res['calculation_option'] = 'directive_terminals'
			return res

		elif row['directive_length'] and row['directive_length'] > 0:
			calculated_points = math.ceil(row['line_length'] / row['directive_length'])
			res = choosing_terminal.get_terminal_from_points_number(calculated_points)
			res['calculation_option'] = 'directive_length'
			return res

		elif row['device_area'] and row['device_area'] > 0:
			calculated_points = math.ceil(row['S_area'] / row['device_area'])
			res = choosing_terminal.get_terminal_from_points_number(calculated_points)
			res['calculation_option'] = 'device_area'
			return res

		else:
			res = choosing_terminal.get_minimum_device_number()
			res['calculation_option'] = 'minimum_terminals'
			return res

	def __join_spaces_and_terminals_DF(self) -> pd.DataFrame:
		joined_df = self._calculation_factory()
		full_base = self.space_and_terminal.merge(joined_df, how='left', on=ColumnChoosing.S_ID)
		return full_base

	def add_k_ef_and_device_flow_to_DF(self) -> pd.DataFrame:
		full_base = self.__join_spaces_and_terminals_DF()
		full_base['k_ef'] = (full_base[self.system_flow] / full_base['minimum_device_number']) / full_base['max_flow']
		full_base['flow_to_device_calculated'] = full_base[self.system_flow] / full_base['minimum_device_number']
		return full_base


class FilteredData:
	def __init__(self, selected_df_data_id, updated_values_data, input_data_df: InputDataDF) -> None:
		self.selected_df_data_id = selected_df_data_id
		self.updated_values_data = updated_values_data
		self.update_parameters_names = input_data_df.device_property_columns_names
		self.parameter_dict = dict(zip(self.update_parameters_names, self.updated_values_data))


class AddPolygonsToDF:

	def __init__(self,
	             df_input_table: pd.DataFrame,
	             level_value: str,
	             input_data_df: InputDataDF
	             ):
		self.to_revit = df_input_table
		self.json_data = input_data_df.json_data
		self.level_value = level_value
		self.input_data_df = input_data_df

	def add_all_polygons_to_df(self):
		all_level_spaces = PolygonMergeBase(self.to_revit, self.json_data, ColumnChoosing.S_level, self.level_value)
		all_level_spaces_filter = all_level_spaces.make_level_filter()
		all_level_spaces_filter['polygon'] = all_level_spaces_filter. \
			apply(lambda df: Polygon([(x, y) for x, y in zip(df.px, df.py)]), axis=1)
		return all_level_spaces_filter


class AddCalculatedPointsToDF(AddPolygonsToDF):
	def __init__(self, df_input_table: pd.DataFrame, level_value: str, system_type: str, input_data_df: InputDataDF):
		super().__init__(df_input_table, level_value, input_data_df)
		self.input_data_df = input_data_df
		self.df_input_table = df_input_table
		self.system_dictionary = input_data_df.system_dictionary
		self.system_type = system_type

	def _make_filter_df(self) -> pd.DataFrame:
		filter_df = FilterEmptySpaceTerminalsInDF(self.system_type, self.input_data_df)
		return filter_df.make_filter_spaces_and_terminals_notnull(self.df_input_table)

	def _get_filtered_level_data_of_spaces_and_devices(self) -> pd.DataFrame:
		filter_df = self._make_filter_df()
		merge_data = PolygonMerge(filter_df, self.json_data,
		                          ColumnChoosing.S_level,
		                          self.level_value,
		                          self.system_dictionary[self.system_type].system_name)
		self.level_df_data = merge_data.make_level_filter()
		return self.level_df_data

	def _add_system_type(self):
		self.level_df_data = self.level_df_data.assign(system_type=self.system_type)
		return self.level_df_data

	def _add_minimum_calculated_devices_to_df(self):
		terminals_calculated = CalculateSpaceTerminalsInDF(self.level_df_data, self.system_type, self.input_data_df)
		self.level_df_data = terminals_calculated.add_k_ef_and_device_flow_to_DF()
		return self.level_df_data

	def _add_polygon_to_df(self) -> pd.DataFrame:
		self.level_df_data['polygon'] = self.level_df_data.apply(
			lambda df: Polygon([(x, y) for x, y in zip(df.px, df.py)]), axis=1
		)
		return self.level_df_data

	def _add_offset_polygon_to_df(self) -> pd.DataFrame:
		self.level_df_data['offset_polygon'] = self.level_df_data.apply(
			lambda df: df.polygon.buffer(-df.wall_offset, join_style=2), axis=1
		)
		return self.level_df_data

	def __polygon_offset_cheking(self, df):
		if isinstance(df.offset_polygon, Polygon):
			return gl.GeometryUtility.get_lines_in_polygon(df.offset_polygon.exterior.coords)
		else:
			ExceptionWriter.exception_wall_offset(
				f'space id = {df[ColumnChoosing.S_ID]}, wall offset = {df["wall_offset"]}')
			return None

	def _add_lines_of_polygon_to_df(self) -> pd.DataFrame:
		self.level_df_data['lines'] = self.level_df_data. \
			apply(lambda df: self.__polygon_offset_cheking(df), axis=1)
		return self.level_df_data

	def _check_line_exist(self):
		self.level_df_data = self.level_df_data[self.level_df_data['lines'].notna()]
		return self.level_df_data

	def _add_curve_length_to_df(self):
		self.level_df_data['line_length'] = self.level_df_data.apply(
			lambda df: InsertTerminals(
				df.lines,
				df.device_orientation_option1,
				df.device_orientation_option2,
				df.single_device_orientation,
				1
			).get_long_curve_length(), axis=1
		)
		return self.level_df_data

	def _add_points_coordinates_to_df(self) -> pd.DataFrame:
		self.level_df_data['points'] = self.level_df_data. \
			apply(lambda df: InsertTerminals(
			df.lines,
			df.device_orientation_option1,
			df.device_orientation_option2,
			df.single_device_orientation,
			df.minimum_device_number
		)
		          .insert_terminals_in_space(), axis=1)
		return self.level_df_data

	def _change_height_of_terminal(self):
		self.level_df_data['pz_new'] = self.level_df_data.apply(lambda df: df.pz[0] - df.ceiling_offset, axis=1)
		return self.level_df_data

	def __add_value_to_tupele_lists(self, tuple_list, add_value):
		if isinstance(tuple_list[0], tuple) or isinstance(tuple_list[0], list):
			new_list = []
			for val in tuple_list:
				temp = val + (add_value,)
				new_list.append(temp)
			return new_list
		else:
			return tuple_list + (add_value,)

	def _add_pz_to_df(self):
		self.level_df_data['instance_points'] = self.level_df_data. \
			apply(lambda df: self.__add_value_to_tupele_lists(df.points, df.pz_new), axis=1)
		return self.level_df_data

	def add_polygon_and_points_to_df(self):
		self._get_filtered_level_data_of_spaces_and_devices()
		self._add_polygon_to_df()
		self._add_offset_polygon_to_df()
		self._add_lines_of_polygon_to_df()
		self._check_line_exist()
		self._add_curve_length_to_df()
		self._add_minimum_calculated_devices_to_df()
		self._add_points_coordinates_to_df()
		self._change_height_of_terminal()
		self._add_pz_to_df()
		return self.level_df_data


class AddFilteredCalculatedPointsToDF(AddCalculatedPointsToDF):
	def __init__(self, level_value: str, system_type: str, filtered_data: FilteredData, input_data_df: InputDataDF):
		"""Update input df with layout view data"""
		super().__init__(level_value, system_type, input_data_df)
		self.filtered_data = filtered_data

	def _make_filter_df(self):
		filter_df = FilterEmptySpaceTerminalsInDF(self.system_type, self.input_data_df)
		filter_not_null_flow = filter_df.make_filter_spaces_and_terminals_notnull()
		updated_df = self._updating_df_from_form_data(filter_not_null_flow)
		return updated_df

	def _updating_df_from_form_data(self, updating_df):
		filter_df_update = DataFrameUpdating(updating_df)
		res = filter_df_update.make_filter_for_updating_device_property_in_df(self.filtered_data.selected_df_data_id,
		                                                                      self.filtered_data.parameter_dict)
		return res

	def _add_minimum_calculated_devices_to_df(self):
		terminals_calculated = CalculateSpaceTerminalsInDF(self.level_df_data, self.system_type, self.input_data_df)
		self.level_df_data = terminals_calculated.add_k_ef_and_device_flow_to_DF()
		return self.level_df_data
