import pandas as pd

from Networks.CalculationNetwork.utility import segment_intersection, split_df_val, p_distance
from Networks.plote_polygons.PolygonMerge import PolygonMerge
from library_hvac_app.list_custom_functions import flatten


class NetworkBuilder:
    def __init__(
        self,
        polygon_merge: PolygonMerge,
        system_location_point: tuple,
        system_name: str,
        sys_flow_column: str,
        network_coordinate_x: tuple,
        network_coordinate_y: tuple,
        route_name: str = "",
        add_row_dict:dict = None
        
        ) -> None:
        """_summary_

        Args:
            polygon_merge (PolygonMerge): _description_
            system_location_point (tuple): _description_
            system_name (str): _description_
            sys_flow_column (str): _description_
            network_coordinate_x (tuple): _description_
            network_coordinate_y (tuple): _description_
            route_name (str, optional): _description_. Defaults to "".
            add_row (pd.DataFrame, optional): _description_. Defaults to None.

            example:
            network_builder1 = NetworkBuilder(
            polygon_merge = polygon_merge,
            system_location_point =  (20000,0),
            system_name = 'S01',
            sys_flow_column ='S_SA_fresh',
            network_coordinate_x = (-25000,25000),
            network_coordinate_y = (3000,3000),
            route_name= 'm_1')
        """

        self.polygon_merge = polygon_merge
        self.system_location_point = system_location_point
        self.system_name = system_name
        self.sys_flow_column = sys_flow_column
        self.system_column_name = polygon_merge.color_filter_name
        self.network_coordinate_x = network_coordinate_x
        self.network_coordinate_y = network_coordinate_y
        self.level_value = polygon_merge.level_val
        self.route_name = route_name
        self.add_row_dict = add_row_dict
        self.polygon_merge.merge_df()
        self.df_branch = self.polygon_merge.make_level_filter()
        self.df_branch = self.make_system_filter(system_name)
        self.concate_additional_row_to_main_df()
        self.calculate()

        """
        create network with intersection of main route and branches.define main route path
        data_dict = nw_default_dict
        """

    def check_additional_row(self,)->list:
        if self.add_row_dict:
            for row_ in self.add_row_dict.keys():
                if self.route_name == row_:
                    return self.add_row_dict[row_]

    def concate_additional_row_to_main_df(self,):
        if self.check_additional_row():

            self.df_branch = pd.concat([self.df_branch, *self.check_additional_row()])
            return self.df_branch


    def __set_attr_to_class(self):
        """
        return attr list
        """
        dict_attr_list = [
            "pcx",
            "pcy",
            "S_ID",
            "x_cross",
            "y_cross",
            "sum_column",
            "branch_dist",
            "rout_dist",
            "m_idx",
            "shift_idx",
        ]
        for attr in dict_attr_list:
            setattr(self, attr, attr)
        return dict_attr_list

    def make_system_filter(self, system_name):
        mask = self.df_branch[self.system_column_name] == system_name
        self.df_branch = self.df_branch[mask]
        return self.df_branch

    @staticmethod
    def add_columns(df, new_columns, new_data):
        """
        add columns for temp df
        """
        df = df.copy()
        for name, val in zip(new_columns, new_data):
            df[name] = val
        return df

    def get_max_layout_dimenstion(self):
        max_limits_data = flatten(self.polygon_merge.min_max_coord("px", "py"))
        return max_limits_data

    def draw_rays_branch(self, px_data_name: str, py_data_name: str):
        """
        create line x,y max,through center polygon point.using polygon_merge.x_min_max,pcy_min,pcy_max
        """
        max_limits_columns = "pcx_min,pcx_max,pcy_min,pcy_max".split(
            ","
        )  # temp columns
        max_limits_data = self.get_max_layout_dimenstion()
        self.df_branch = self.add_columns(
            self.df_branch, max_limits_columns, max_limits_data
        )
        # unpack min-max limit data
        branch_ray_data_y = (
            self.df_branch["pcx_min"],
            self.df_branch["pcx_max"],
            self.df_branch[self.pcy],
            self.df_branch[self.pcy],
        )
        branch_ray_data_x = (
            self.df_branch[self.pcx],
            self.df_branch[self.pcx],
            self.df_branch["pcy_min"],
            self.df_branch["pcy_max"],
        )
        self.df_branch[px_data_name] = [[*arg] for arg in zip(*branch_ray_data_y)]
        self.df_branch[py_data_name] = [[*arg] for arg in zip(*branch_ray_data_x)]
        self.df_branch = self.df_branch.drop(max_limits_columns, axis=1)
        return self.df_branch

    def get_intersection(
        self, new_name, df_ray_name, main_rout_coord_x, main_rout_coord_y
        ):
        """
        get intersection through draw_rays_branch. Input data is main_rout_coord = x1,x2,y1,y2
        """
        self.df_branch[new_name] = self.df_branch.apply(
            lambda x: segment_intersection(
                *x[df_ray_name], *main_rout_coord_x, *main_rout_coord_y
            ),
            axis=1,
        )
        return self.df_branch[new_name]

    def split_coord(self, splited_column: str, pref: str = ""):
        """
        utility func for spliting coordinates from intersection
        """
        x_coor_name = splited_column + "_x" + pref
        y_coor_name = splited_column + "_y" + pref
        split_df_val(self.df_branch, splited_column, x_coor_name, y_coor_name)
        return x_coor_name, y_coor_name

    def drop_nan_intersection(self, column_name: str):
        """
        drop empty rows of choosen intersection column
        """
        self.df_branch.dropna(subset=[column_name], inplace=True)

    def get_intersect_distance(
        self,
        px_col_name: str,
        py_col_name: str,
        intersect_column: str,
        new_col_name: str,
        pref: str = "",
        ):
        """
        calculate distance between  point and intersection point
        """
        self.x_coor_name, self.y_coor_name = self.split_coord(
            intersect_column,
        )
        self.df_branch[new_col_name + pref] = self.df_branch.apply(
            lambda x: p_distance(
                x[px_col_name], x[py_col_name], x[self.x_coor_name], x[self.y_coor_name]
            )
            if x[self.x_coor_name] != None and x[self.y_coor_name] != None
            else None,
            axis=1,
        )
        return self.df_branch

    def get_main_point_dist(
        self,
        px_: int,
        py_: int,
        intersect_column: str,
        new_col_name: str,
        pref: str = "",
        ):
        """
        calculate distance between  point and intersection point
        """

        self.df_branch[new_col_name + pref] = self.df_branch.apply(
            lambda x: p_distance(px_, py_, x[self.x_coor_name], x[self.y_coor_name])
            if x[self.x_coor_name] != None and x[self.y_coor_name] != None
            else None,
            axis=1,
        )
        return self.df_branch

    def shift_and_sort_route(
        self, main_root_distance, main_idx, shift_idx, m_prefix="m_"
        ):
        """
        shifting intersection point and sorting data by distance
        input new columns names
        "rout_dist","m_idx","shift_idx",m_prefix="m1_"
        """
        self.df_branch = self.df_branch.sort_values(by=[main_root_distance])
        self.df_branch.reset_index(drop=True, inplace=True)
        self.df_branch[main_idx] = m_prefix + self.df_branch.index.astype(str)
        self.df_branch[shift_idx] = self.df_branch[main_idx].shift(1)
        self.df_branch[shift_idx] = self.df_branch[shift_idx].fillna(
            value=m_prefix + "cent"
        )
        return self.df_branch

    def get_cumsum(self, sum_column_name):
        """
        sort by distance and get cumsum from main_root
        "sum_column" - new column
        """
        self.df_branch.sort_index(inplace=True, ascending=False)
        self.df_branch[sum_column_name] = self.df_branch[self.sys_flow_column].cumsum()
        return self.df_branch

    def choose_loacation_type(self, x1, x2, y1, y2):
        if x1 == x2:
            return "v"
        elif y1 == y2:
            return "h"
        else:
            raise ValueError("the line must be horizontal or vertical ")

    def create_intersection_chain(
        self, main_rout_coord_x: tuple, main_rout_coord_y: tuple, prefix: str = ""
        ):
        """
        make all intersection with main route.
        Get summ of branch_load.route_loacation_type = "h","v" (horizontal,vertical)
        """
        route_loacation_type = self.choose_loacation_type(
            *main_rout_coord_x, *main_rout_coord_y
        )
        self.prefix = prefix
        self.main_rout_coord_x = main_rout_coord_x
        self.main_rout_coord_y = main_rout_coord_y
        self.check_intersection = (
            self.x_cross if route_loacation_type == "v" else self.y_cross
        )
        self.draw_rays_branch("pcx_branch_max", "pcy_branch_max")
        self.get_intersection(
            self.x_cross,
            "pcx_branch_max",
            self.main_rout_coord_x,
            self.main_rout_coord_y,
        )
        self.get_intersection(
            self.y_cross,
            "pcy_branch_max",
            self.main_rout_coord_x,
            self.main_rout_coord_y,
        )
        self.x_intersect = self.split_coord(self.check_intersection)[0]
        self.y_intersect = self.split_coord(self.check_intersection)[1]
        self.drop_nan_intersection(self.check_intersection)
        self.get_intersect_distance(
            self.pcx, self.pcy, self.check_intersection, self.branch_dist
        )
        self.get_main_point_dist(
            *self.system_location_point, self.check_intersection, self.rout_dist
        )
        return self.df_branch

    def shift_and_get_cumsum(self):
        self.shift_and_sort_route(
            self.rout_dist, self.m_idx, self.shift_idx, m_prefix=self.prefix
        )
        return self.get_cumsum(self.sum_column)

    def filtred_df(self):
        self.main_columns = [
            self.S_ID,
            self.pcx,
            self.pcy,
            self.sys_flow_column,
            self.level_value,
            self.x_intersect,
            self.y_intersect,
            self.branch_dist,
            self.rout_dist,
            self.m_idx,
            self.shift_idx,
            self.sum_column,
            "S_Name",
            'S_Number'
        ]

        self.df_branch = self.df_branch.filter(self.main_columns)
        return self.df_branch

    def __sub__(self, other):
        """
        delate intersection with main route if we have some routs
        """
        if isinstance(other, NetworkBuilder):
            merge_df = self.df_branch.merge(
                other.df_branch, how="left", on=self.S_ID, suffixes=("", "_DROP")
            )
            merge_df["togel"] = (
                merge_df[self.branch_dist] - merge_df["branch_dist_DROP"]
            )
            merge_df = merge_df[[self.S_ID, "togel"]]
            df_branch = self.df_branch.merge(merge_df, how="left", on=self.S_ID)
            df_branch = df_branch[
                (df_branch["togel"] <= 0) | (df_branch["togel"].isnull())
            ]
            self.df_branch = df_branch.drop(columns="togel")
            return self.shift_and_get_cumsum()
        else:
            return ValueError

    def crete_network(self):
        self.create_intersection_chain(
            self.network_coordinate_x, self.network_coordinate_y, self.route_name
        )
        self.shift_and_get_cumsum()
        self.df_branch = self.filtred_df()

    def create_location_route(self):
        sum_value_filter = self.df_branch[self.shift_idx].str.contains("cent", regex=False)
        sum_value = self.df_branch[sum_value_filter][self.sum_column]
        new_row = {
            self.x_intersect : self.system_location_point[0],
            self.y_intersect : self.system_location_point[1],
            # self.sum_column : sum_value,
            self.pcx : self.df_branch[sum_value_filter][self.x_intersect],
            self.pcy : self.df_branch[sum_value_filter][self.y_intersect],
            self.sys_flow_column: sum_value,
            self.S_ID:'loaction'
            }
        self.df_branch = self.df_branch.append(pd.DataFrame(new_row), ignore_index=True)
        return self.df_branch


    def create_additional_route(self):
        filter_name =  self.df_branch[self.shift_idx].str.contains('cent', regex=False)
        df_additional_route = self.df_branch[filter_name]
        df_additional_route = df_additional_route.filter(
            [
                self.shift_idx,
                self.x_intersect,
                self.y_intersect,
                self.sum_column,
            ]
        )
        renamed_dict = {
            self.shift_idx: self.S_ID,
            self.x_intersect: self.pcx,
            self.y_intersect: self.pcy,
            self.sum_column: self.sys_flow_column,
        }
        df_additional_route = df_additional_route.rename(renamed_dict, axis=1)
        return df_additional_route

    def calculate(self):
        self.__set_attr_to_class()
        self.crete_network()
