import os

import pandas as pd
from Networks.plote_polygons.SetColor import *

from Networks.plote_polygons.SetColor import SetColor
from library_hvac_app.files_custom_functions import Loader
from library_hvac_app.list_custom_functions import flatten


class PolygonMerge:
    def __init__(self, in_df:pd.DataFrame,
                json_path:os.path,
                color_filter_name,
                level_column,
                level_val) -> None:
        """merge json file and df to revit. calculate min max coordinates

        Args:
            in_df (pd.DataFrame): _description_
            json_path (os.path): _description_
            color_filter_name (_type_): _description_
            level_column (_type_): _description_
            level_val (_type_): _description_
        """
        self.in_df = in_df
        self.json_path = json_path
        self.color_filter_name = color_filter_name
        self.level_column, self.level_val = level_column, level_val

    def add_color_to_df(self):
        """ From inst class SetColor 
        add color to each row by filtred column"""
        self.color = SetColor(self.in_df, self.color_filter_name, idx="S_ID")
        self.color.set_color_by_category()
        return self.color.merge_color_df()

    def load_json(self)->pd.DataFrame:
        """to df

        Returns:
            pd.DataFrame.: for merge
        """
        load = Loader(self.json_path)
        df_load = load.load_json_pd()
        return df_load

    def merge_df(self):
        color_df = self.add_color_to_df()
        self.d_merge = self.load_json().merge(color_df, on="S_ID")
        self.d_merge['S_ID'] = self.d_merge['S_ID'].astype(str)
        return self.d_merge

    def make_level_filter(self):
        mask = self.d_merge[self.level_column] == self.level_val
        self.d_merge = self.d_merge[mask]

        return self.d_merge

    def list_value_points(self, column_name):
        list_val = self.d_merge[column_name].values
        list_val_fl = flatten(list_val)
        return list_val_fl

    def min_max_bord(self, list_val: list, k=0.3):
        """
        define min and max point for plot dim
        """
        x_max = max(list_val)
        x_min = min(list_val)
        x_mx = abs(x_max)
        x_mn = abs(x_min)
        x_max_abs = (x_mx+x_mx*k)
        x_min_abs = (x_mn+x_mn*k)

        def return_value(in_value, reform_value):
            if in_value > 0:
                return reform_value
            else:
                return -1*reform_value
        res_min = return_value(x_min, x_min_abs)
        res_max = return_value(x_max, x_max_abs)
        return res_min, res_max

    def min_max_coord(self, px_col_name="px", py_col_name="py"):
        x = self.min_max_bord(self.list_value_points(px_col_name))
        y = self.min_max_bord(self.list_value_points(py_col_name))
        return x, y
