import pandas as pd

from library_hvac_app.files_custom_functions import Loader


class NetworkLevelValue:

	def __init__(self, json_polygons: str, revit_export: pd.DataFrame, S_ID: str = "S_ID", level_column_name="S_level",
	             pz_column_name="pz"):
		self._revit_export = revit_export
		self._S_ID = S_ID
		self._level_column_name = level_column_name
		self._pz_column_name = pz_column_name
		load = Loader(json_polygons)
		self._df_load = load.load_json_pd()
		self._df_load[S_ID] = self._df_load[S_ID].astype(str)
		self._revit_export[S_ID] = self._revit_export[S_ID].astype(str)

	@property
	def merge_df(self):
		merge_df = self._df_load.merge(self._revit_export, on=self._S_ID)
		merge_df[self._pz_column_name] = merge_df[self._pz_column_name].apply(
			lambda x: x[0] if isinstance(x, list) else x)
		return merge_df

	@property
	def df_dict(self):
		group_df = self.merge_df.groupby([self._pz_column_name, self._level_column_name]).agg("count").reset_index()
		df_dict = dict(zip(group_df[self._level_column_name], group_df[self._pz_column_name]))
		return df_dict
