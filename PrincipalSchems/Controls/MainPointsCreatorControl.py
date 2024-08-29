import pandas as pd

from PrincipalSchems.Controls.WidgetsModelControl import WidgetsModelControl
from PrincipalSchems.Models.ConstantModel import SystemProperty
from PrincipalSchems.Models.Models import PolygonMainModel, PointsMainModel
from PrincipalSchems.View.MainLayoutView import TabsView
from Utility.SystemGroupCreator import SystemGroupCreator
from library_hvac_app.list_custom_functions import flatten


class MainPointsCreatorControl:
    def __init__(
            self,
            input_df: pd.DataFrame,
            tab_view: TabsView,
            step_x: int = 50,
            step_y: int = 50,
    ):
        # calculate start end points with layout data

        self.input_df = input_df.copy()
        self.layout_view_context_data = tab_view.layout_view_context_data
        self.tab_view = tab_view
        self.all_levels = input_df[self.layout_view_context_data.level_column]
        self.step_x = step_x
        self.step_y = step_y

    def _calculate_max_space_number_in_level(self) -> None:
        """get maximum spaces on level. for calculate max point for vertical system line"""
        self.line_direction = self.layout_view_context_data.vertical_direction_list
        self.system_direction = self.layout_view_context_data.horizontal_direction_list
        self.max_space_count = (
            self.input_df.groupby(self.layout_view_context_data.level_column)["S_ID"]
            .count()
            .max()
        )

        return self.max_space_count

    def calculate_points(self):
        self._calculate_max_space_number_in_level()
        step = 0
        all_level_points = []
        shapely_polygons = []
        self.polygon_property = {}

        for level_ in self.all_levels.unique():
            filter_level_df = self.input_df.loc[self.all_levels == level_]

            df_dict = SystemGroupCreator.create_dictionary_from_df(
                filter_level_df, self.layout_view_context_data.main_columns
            )
            # df_property = WigetsModelControl.add_start_wiget_property(
            #     df_dict, dynamic_layout_view_context_data.base_property_wiget
            # )
            df_property = (
                WidgetsModelControl.create_and_add_property_to_system_property(
                    self.input_df, self.tab_view
                )
            )
            polygon_main_model = PolygonMainModel(
                df_dict,
                step,
                self.max_space_count,
                step_x=self.step_x,
                step_y=self.step_y,
            )
            points_model = PointsMainModel(df_property, polygon_main_model)
            all_points = points_model.get_system_points(
                self.line_direction, self.system_direction
            )
            self.polygon_property.update(polygon_main_model.polygon_property)
            step += self.layout_view_context_data.level_distance

            all_level_points.append(all_points)
            shapely_polygons.append(polygon_main_model.polygon_dict.values())
        self.system_property_points: list[SystemProperty] = flatten(all_level_points)

        self.flatten_shapely_polygons = flatten(shapely_polygons)

        return self.system_property_points, self.flatten_shapely_polygons, self.polygon_property