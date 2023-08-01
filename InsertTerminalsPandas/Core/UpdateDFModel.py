from InsertTerminalsPandas.InputData.input import *
from StaticData.Exception import *


class DataFrameUpdating:
	def __init__(self, input_df: pd.DataFrame) -> None:
		"""update df from ui choosing data

        Args:
            input_df (pd.DataFrame): level df data
          """
		self.input_df = input_df

	def _make_filter_df_by_value_list(self, selected_df_data_id) -> pd.DataFrame:
		if selected_df_data_id:
			df_temp = self.input_df.copy()
			self.condition = df_temp[ColumnChoosing.S_ID].astype(str).isin([str(val) for val in selected_df_data_id])
			df_temp_out = df_temp[self.condition]
			return df_temp_out
		else:
			return self.input_df

	def make_filter_for_updating_device_property_in_df(self, selected_df_data_id, update_dict: dict):
		df_temp = self._make_filter_df_by_value_list(selected_df_data_id)
		if df_temp.empty:
			ExceptionWriter.exception_name_and_flow(selected_df_data_id)
		for param_name in update_dict.keys():
			df_temp.loc[self.condition, param_name] = update_dict[param_name]
		return df_temp

	def _update_df_(self, init_df: pd.DataFrame, joined_df: pd.DataFrame):
		return init_df.update(joined_df)
