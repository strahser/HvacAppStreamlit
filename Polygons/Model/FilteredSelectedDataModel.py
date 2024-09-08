import pandas as pd


class FilteredSelectedDataModel:
	def __init__(self, merge_df: pd.DataFrame, level_column_name: str, level_names, id_for_color_filter: str):
		"""Take input df. Get plotly coordinates. Lookup row id in df by plotly coordinates
		 Choose row from data frame by coordinates and level value"""
		self.merge_df = merge_df
		self.level_column_name = level_column_name
		self.level_names = level_names
		self.id_for_color_filter = id_for_color_filter

	def __transform_plotly_coordinates_to_id(self, selected_values: dict):
		if isinstance(selected_values, dict) and 'x' in selected_values.keys() and 'y' in selected_values.keys():
			cond_x = self.merge_df["pcx"] == selected_values['x']
			cond_y = self.merge_df["pcy"] == selected_values['y']
			cond_level = self.merge_df[self.level_column_name] == self.level_names
			selected_id = list(self.merge_df.loc[cond_x & cond_y & cond_level][self.id_for_color_filter].values)
			return selected_id[0]

	def get_selected_id(self, selected_values: list[dict]):
		""" get id from px,py level name in df in loop of list dict of selected values"""
		if selected_values:
			for select_id in selected_values:
				id_ = self.__transform_plotly_coordinates_to_id(select_id)
				if id_:
					return id_
