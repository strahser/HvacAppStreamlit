import os

import pandas as pd
from library_hvac_app.files_custom_functions import Loader
from Polygons.PolygonPlot.SetColor import SetColor
from Polygons.PolygonPlot.PolygonMergeStatic import MergedIdProperty


class PolygonMerge:
	def __init__(self, in_df: pd.DataFrame,
				geometry_data: os.path,
				color_filter_name,
				level_column=None,
				level_val=None,
				merged_df_id=MergedIdProperty.merged_df_id,
				json_id = MergedIdProperty.json_id
	             ) -> None:
		"""merge json file and df to revit. calculate min max coordinates
        """
		self.d_merge = None
		self.in_df = in_df.copy()
		self.geometry_data = geometry_data
		self.color_filter_name = color_filter_name
		self.level_column, self.level_val = level_column, level_val
		self.merged_df_id = merged_df_id
		self.json_id = json_id
	
	def merge_df(self):
		color_df = self._add_color_to_df()
		self.d_merge = self._load_geometry_data().merge(color_df,
		                                                left_on=self.json_id,
		                                                right_on=self.merged_df_id)
		self.d_merge[self.merged_df_id] = self.d_merge[self.merged_df_id].astype(str)
		return self.d_merge
	
	def _add_color_to_df(self):
		""" From inst class SetColor
        add color to each row by filtered column"""
		self.color = SetColor(self.in_df, self.color_filter_name, idx=self.merged_df_id)
		self.color.set_color_by_category()
		return self.color.merge_color_df()
	
	def _load_geometry_data(self) -> pd.DataFrame:
		"""to df

        Returns:
            pd.DataFrame.: for merge
        """
		if isinstance(self.geometry_data, pd.DataFrame):
			return self.geometry_data
		else:
			load = Loader(self.geometry_data)
			df_load = load.load_json_pd()
			return df_load
	
	def make_level_filter(self):
		mask = self.d_merge[self.level_column] == self.level_val
		self.d_merge = self.d_merge[mask]
		
		return self.d_merge
