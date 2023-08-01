from PolygonMerge import *

import math


class PolygonLimits:

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


class PolygonPlotter:
    def __init__(self, polygon_merge: PolygonMerge, show_grid=False) -> None:
        """draw polygons and add text to polygons

        Args:
            polygon_merge (PolygonMerge): df with coordinates polygon and color for fill
            show_grid (bool, optional): _description_. Defaults to False.
        """

        self.fig, self.ax = mpl_fig_setting(show_grid)
        self.polygon_merge = polygon_merge
        self._df = self.polygon_merge.merge_df()
        self.level_column = self.polygon_merge.level_column
        self.level_val = self.polygon_merge.level_val

        self.color_filter_name = self.polygon_merge.color_filter_name
        max_coordinates = flatten(PolygonLimits().min_max_coord("px", "py"))
        self.x_min_max = max_coordinates[0], max_coordinates[1]
        self.y_min_max = max_coordinates[2], max_coordinates[3]

    def make_level_filter(self):
        self._df = self._df[self._df[self.level_column] == self.level_val]
        return self._df

    def __draw_all_lines(self):
        """for testin and future exstation
        """
        for x_val, y_val in zip(self._df[self.pcx], self._df[self.pcx]):
            self.ax.plot((x_val, x_val), (self.ax.get_ylim()),
                        color='r', linestyle='-.', linewidth=3, label='branch')
            self.ax.plot((self.ax.get_xlim()), (y_val, y_val),
                        color='b', linestyle='-.', linewidth=3, label='branch')
        self.ax.plot(self.ax.get_xlim(), (0, 0), linestyle='-.',
                    color='green', linewidth=7, label='main')

    def create_polygon_data(self, new_zip_coord_name="polygon_coord", pol_x="px", pol_y="py"):
        """
        create new column for zip(x,y) polygon coordinates from json polygon coordinates px,py
        """
        self._df = self._df.assign(polygon_coord=self._df.apply(lambda x:
                                                                list(zip(x[pol_x], x[pol_y])), axis=1)
                                )
        return self._df

    def draw_polygons(self, poly_data_column: str, color_column: str, is_filled: bool = True):
        is_filled = bool(is_filled)
        for val, color, lable in zip(self._df[poly_data_column], self._df[color_column], self._df[self.color_filter_name]):
            p = Polygon(val, color=color, fill=is_filled, label=lable)
            self.ax.add_patch(p)

    def add_coordinate_axise(self):
        self.ax.set_xlim(*self.x_min_max)
        self.ax.set_ylim(*self.y_min_max)

    def add_ticks(self):
        self.ax.set_xticks(
            np.arange(*self.x_min_max, math.ceil(self.x_min_max[1]/10)))
        self.ax.set_yticks(
            np.arange(*self.y_min_max, math.ceil(self.y_min_max[1]/10)))

    def add_title(self):
        self.ax.set_title(f'Layout of {self.level_val}. Category {self.color_filter_name}.',
                        fontsize=20, style='italic', weight="bold")

    @staticmethod
    def round_for_str(val):
        try:
            res = round(val)
        except:
            res = val
        return res

    def add_text_from_df(
            self,
            df_,
            x_coor_column,
            y_coor_column,
            prefix_list: str,
            column_list,
            **kwargs):
        """
        join string columns from df and add prefix
        """
        column_list = to_list(column_list)
        prefix_list = prefix_list.split(",") if isinstance(
            prefix_list, str) else prefix_list
        df_ = df_.assign(temp="").copy()
        if len(prefix_list) == len(column_list):
            for pref, colum in zip(prefix_list, column_list):
                temp_str = pref + df_[colum]\
                    .apply(lambda x: self.round_for_str(x)).astype(str)+"\n"
                df_["temp"] = df_["temp"].astype(str).str.cat(temp_str)
                [
                    self.ax.text(x, y, txt, kwargs) for x, y, txt in zip(
                        df_[x_coor_column], df_[y_coor_column], df_["temp"])
                ]
            df_ = df_.drop("temp", axis=1)
            return df_
        else:
            for colum in column_list:
                temp_str = df_[colum]\
                    .apply(lambda x: self.round_for_str(x)).astype(str)+"\n"
                df_["temp"] = df_["temp"].astype(str).str.cat(temp_str)
                [
                    self.ax.text(x, y, txt, kwargs) for x, y, txt in zip(
                        df_[x_coor_column], df_[y_coor_column], df_["temp"])
                ]
            df_ = df_.drop("temp", axis=1)
            return df_

    @staticmethod
    def save_plote(fig):
        img = io.StringIO()
        fig.savefig(img, format='svg')
        # clip off the xml headers from the image
        svg_img = '<svg' + img.getvalue().split('<svg')[1]
        return svg_img

    def plot_polygons(self, text_prefix: str = '', column_list: list = [], is_filled: bool = True):
        """
        call methodes for plot polygons by level and color and add text
        """
        self.make_level_filter()
        self.add_coordinate_axise()
        self.create_polygon_data()
        self.draw_polygons("polygon_coord", "color", is_filled=is_filled)
        self.add_title()
        self.ax.legend()
        self.add_text_from_df(
            self._df,
            "pcx", "pcy",
            text_prefix,
            column_list,
            bbox=box_1, **text_style)
        return self.fig
