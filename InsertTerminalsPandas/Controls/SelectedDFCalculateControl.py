from InsertTerminalsPandas.TermilalView.ConfigView import ConfigView, InputDataDF,  pd
from InsertTerminalsPandas.Core.AddDataToDF import  AddCalculatedPointsToDF, \
	FilterEmptySpaceTerminalsInDF, FilteredData, AddFilteredCalculatedPointsToDF
from InsertTerminalsPandas.Static.DFStylesCondition import style_less_then
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing


class MainDFCalculate:
	def __init__(self,
	             config_layout: ConfigView,
	             system_type: str,
	             level_value: str = None,
	             input_data_df_val=InputDataDF
	             ):
		self.config_layout = config_layout
		self.system_type = system_type
		self.level_value = level_value if level_value else self.config_layout.level_value
		self.system_name = input_data_df_val.system_dictionary[self.system_type].system_name
		self.input_data_df = input_data_df_val

	def _create_df_calculated(self, input_df_table: pd.DataFrame):
		self.df_calculated = AddCalculatedPointsToDF(
			level_value=self.level_value,
			df_input_table=input_df_table,
			system_type=self.system_type,
			input_data_df=self.input_data_df
		)
		self.df_calculated.add_polygon_and_points_to_df()
		return self.df_calculated

	def _check_is_selected_id_has_flow(self, filtered_data):
		filter_df = FilterEmptySpaceTerminalsInDF(self.df_calculated.system_type, self.input_data_df)
		filter_not_null_flow = filter_df.make_filter_spaces_and_terminals_notnull()
		condition = (filtered_data.selected_df_data_id and
		             filter_not_null_flow[ColumnChoosing.S_ID].isin(filtered_data.selected_df_data_id).any())
		if condition:
			return True
		else:
			return False

	def _create_df_filtered_calculated(self):

		filtered_data = FilteredData(
			self.config_layout.selected_df_data_id,
			self.input_data_df
		)
		self.df_calculated = AddFilteredCalculatedPointsToDF(
			level_value=self.level_value,
			system_type=self.system_type,
			filtered_data=filtered_data,
			input_data_df=self.input_data_df
		)
		if self._check_is_selected_id_has_flow(filtered_data):
			self.df_calculated.add_polygon_and_points_to_df()
			return self.df_calculated
		else:
			return self.df_calculated.add_polygon_and_points_to_df()

	def __check_is_selected_df_data_id_exist(self):
		if hasattr(self.config_layout, 'selected_df_data_id'):
			return True
		else:
			return False

	def _choose_calculation_data(self):
		if self.__check_is_selected_df_data_id_exist() and self.config_layout.selected_df_data_id:
			return self._create_df_filtered_calculated()
		else:
			return self._create_df_calculated(self.input_data_df.revit_export)

	def get_df_result(self):
		self._choose_calculation_data()
		result_columns = self.input_data_df.df_device_result_columns + [self.system_name]
		df_result = self.df_calculated.level_df_data[result_columns].style.applymap(style_less_then, subset='k_ef')
		return df_result

	def get_df_for_concat(self):
		df_result = self.df_calculated.level_df_data.rename(columns={self.system_name: 'system_name'})
		return df_result
