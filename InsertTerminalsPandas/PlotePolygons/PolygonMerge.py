import os

from InsertTerminalsPandas.PlotePolygons.SetColor import *

from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
from library_hvac_app.DbFunction.pandas_custom_function import Loader


class PolygonMergeBase:
	def __init__(self, in_df: pd.DataFrame,
	             json_path: os.path,
	             level_column,
	             level_val):
		"""merge json file and df to revit. calculate min max coordinates

        Args:
            in_df (pd.DataFrame): _description_
            json_path (os.path): _description_
            level_column (_type_): _description_
            level_val (_type_): _description_
        """
		self.in_df = in_df
		self.json_path = json_path
		self.level_column = level_column
		self.level_val = level_val

	def load_json(self) -> pd.DataFrame:
		"""to df

        Returns:
            pd.DataFrame.: for merge
        """
		load = Loader(self.json_path)
		df_load = load.load_json_pd()
		return df_load

	def merge_df(self) -> pd.DataFrame:
		self.in_df[ColumnChoosing.S_ID] = self.in_df[ColumnChoosing.S_ID].astype(str)
		self.load_json()[ColumnChoosing.S_ID] = self.load_json()[ColumnChoosing.S_ID].astype(str)
		df_merge = self.in_df.merge(self.load_json(), on="S_ID")
		return df_merge

	def make_level_filter(self) -> pd.DataFrame:
		df_merge = self.merge_df()
		mask = df_merge[self.level_column] == self.level_val
		df_merge = df_merge[mask]
		return df_merge


class PolygonMerge(PolygonMergeBase):
	def __init__(self, in_df: pd.DataFrame, json_path: os.path, level_column, level_val, color_filter_name) -> None:
		super().__init__(in_df, json_path, level_column, level_val)
		"""add color column to DF
        Args:
            color_filter_name (str): column in df for color filter
        """
		self.color_filter_name = color_filter_name

	def merge_df(self):
		color_df = self.add_color_to_df()
		df_merge = self.load_json().merge(color_df, on="S_ID")
		df_merge[ColumnChoosing.S_ID] = df_merge[ColumnChoosing.S_ID].astype(str)
		return df_merge

	def add_color_to_df(self):
		""" From inst class SetColor
        add color to each row by filtered column"""
		self.color = SetColor(self.in_df, self.color_filter_name, idx="S_ID")
		self.color.set_color_by_category()
		return self.color.merge_color_df()
