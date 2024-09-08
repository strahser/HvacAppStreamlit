from library_hvac_app.list_custom_functions import flatten
import pandas as pd


class PlotBoardDimension:
	@staticmethod
	def get_columns_list_value(input_df: pd.DataFrame, column_name: str):
		list_val = input_df[column_name].values
		list_val_fl = flatten(list_val)
		return list_val_fl
	
	@staticmethod
	def min_max_bord(list_val: list, k=0.3):
		"""
        define min and max point for plot dim
        """
		x_max = max(list_val)
		x_min = min(list_val)
		x_mx = abs(x_max)
		x_mn = abs(x_min)
		x_max_abs = (x_mx + x_mx * k)
		x_min_abs = (x_mn + x_mn * k)
		
		def return_value(in_value, reform_value):
			if in_value > 0:
				return reform_value
			else:
				return -1 * reform_value
		
		res_min = return_value(x_min, x_min_abs)
		res_max = return_value(x_max, x_max_abs)
		return res_min, res_max
	
	def min_max_coord(self, input_df: pd.DataFrame, px_col_name="px", py_col_name="py"):
		x = self.min_max_bord(self.get_columns_list_value(input_df, px_col_name))
		y = self.min_max_bord(self.get_columns_list_value(input_df, py_col_name))
		return x, y
