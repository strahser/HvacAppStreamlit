import numpy as np
import pandas as pd

from Polygons.PolygonPlot.PolygonMerge import PolygonMerge
from PrincipalSchems.Controls.MainPointsCreatorControl import MainPointsCreatorControl
from PrincipalSchems.Controls.WidgetsModelControl import WidgetsModelControl
from PrincipalSchems.Models.ConstantModel import LevelPropertyModel
from PrincipalSchems.View.MainLayoutView import TabsView, LayoutViewContextData, DynamicLayoutViewContextData
from Utility.TextWorker import TextWorkerForPlot


class PolygonPointsMergeControl:
    def __init__(self, input_df: pd.DataFrame, tabs_view: TabsView) -> None:
        """add start,end points,color from callback widgets  to df for plotting

        """
        self.system_list = None
        self.add_color_df = None
        self.input_df = input_df
        self.tabs_view = tabs_view
        self.layout_view_context_data = LayoutViewContextData(tabs_view.system_and_flow_view, tabs_view.static_layout)
        self.dynamic_layout_context_data = DynamicLayoutViewContextData(tabs_view.dynamic_layout)
        self.main_points_creator = MainPointsCreatorControl(
            self.input_df,
            self.tabs_view,
            step_x=self.layout_view_context_data.polygon_width,
            step_y=self.layout_view_context_data.polygon_height,
        )

    def get_level_property(self) -> list[LevelPropertyModel]:
        polygon_width = self.tabs_view.static_layout.space_dimension_view.polygon_width
        system_dist = self.tabs_view.static_layout.space_dimension_view.distance_between_systems
        vertical_direction_list = self.tabs_view.layout_view_context_data.vertical_direction_list
        level_x = polygon_width * self.main_points_creator.max_space_count / 2
        level_property_list: list[LevelPropertyModel] = []
        for level_ in self.main_points_creator.all_levels.unique():
            level_property = LevelPropertyModel()
            system_y = max([val.y_end_points for val in self.system_property_points if val.level_value == level_])
            level_property.system_y = system_y
            level_property.level_name = level_
            level_property.level_coord_x = level_x
            level_property.level_coord_y = system_y + system_dist
            level_property.vertical_direction_list = vertical_direction_list
            level_property_list.append(level_property)
        return level_property_list

    def _get_start_end_system_points(self) -> None:
        self.main_points_creator.calculate_points()
        self.system_property_points = self.main_points_creator.system_property_points
        flatten_shapely_polygons = self.main_points_creator.flatten_shapely_polygons
        self.polygon_dict = self.main_points_creator.polygon_property

    def _add_start_end_system_points_to_df(self) -> pd.DataFrame:
        df_system_property_points = pd.DataFrame(
            {
                "S_ID": [p.space_id for p in self.system_property_points],
                "system_name": [p.system_name for p in self.system_property_points],
                "p_x": [p.offset_point_x for p in self.system_property_points],
                "p_y": [p.offset_point_y for p in self.system_property_points],
            }
        )
        level_df = self.input_df[["S_ID", self.layout_view_context_data.level_column]]
        df_system_property_points_merge = df_system_property_points.merge(
            level_df, how="left", on="S_ID"
        )
        return df_system_property_points_merge

    def _get_system_points_between_levels(self) -> pd.DataFrame:
        df_level_points = (
            self._add_start_end_system_points_to_df()
            .groupby(["system_name"])
            .agg(
                Max_x=("p_x", np.max),
                Min_x=("p_x", np.min),
                Max_y=("p_y", np.max),
                Min_y=("p_y", np.min),
            )
            .reset_index()
        )
        return df_level_points

    def _add_system_color_to_df(self, dynamic_layout_view_context_data: DynamicLayoutViewContextData) -> pd.DataFrame:
        df_level_points = self._get_system_points_between_levels()
        df_level_points["color"] = df_level_points.apply(
            lambda df: WidgetsModelControl.add_color_to_widget(
                dynamic_layout_view_context_data.base_property_widget, df["system_name"]
            ),
            axis=1,
        )
        return df_level_points

    @property
    def polygon_merge_df(self) -> pd.DataFrame:
        """получаем px,py,pcx,pcy,color"""
        polygon_merge = PolygonMerge(
            self.input_df,
            self.polygon_dict,
            self.layout_view_context_data.space_data_view.color_filter_name,
        )
        return polygon_merge.merge_df()

    @property
    def text_worker(self) -> TextWorkerForPlot:
        pl_layout = self.layout_view_context_data.space_data_view
        text_worker = TextWorkerForPlot(self.polygon_merge_df)
        text_worker.concat_value_with_prefix(pl_layout.space_prefix, pl_layout.space_suffix, pl_layout.space_value)
        return text_worker

    def calculate(self) -> None:
        self._get_start_end_system_points()
        self.add_color_df = self._add_system_color_to_df(self.dynamic_layout_context_data)
        self.system_list: list[pd.DataFrame] = self.dynamic_layout_context_data.unique_systems["system"].tolist()
