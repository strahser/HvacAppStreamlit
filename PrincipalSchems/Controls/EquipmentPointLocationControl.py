import pandas as pd

from PrincipalSchems.Controls.PolygonPointsMergeControl import PolygonPointsMergeControl
from PrincipalSchems.Models.Models import SystemLocationModelBase, ExistLevelLocationModel, NewLevelLocationModel
from PrincipalSchems.View.MainLayoutView import DynamicWidgetsViewContextData


class EquipmentPointLocationControl:
    def __init__(self, polygon_points_merge_control: PolygonPointsMergeControl):
        self.polygon_points_merge_control = polygon_points_merge_control

    def __create_equipment_location_point(
            self,
            system: str,
            level: str,
    ) -> pd.DataFrame:
        """create equipment new point(up or down point to exist level) or exist point(horizontal point)"""

        system_model = SystemLocationModelBase(
            self.polygon_points_merge_control.system_property_points,
            self.polygon_points_merge_control.input_df,
            system,
            level,
            self.polygon_points_merge_control.layout_view_context_data.level_column,
        )

        if system_model._is_equipment_level_in_system_level():
            exist_level_model = ExistLevelLocationModel(system_model)
            model_unique_level = exist_level_model.create_exist_level_equipment_base_point(
                self.polygon_points_merge_control.layout_view_context_data.horizontal_direction_list,
                self.polygon_points_merge_control.layout_view_context_data.equipment_horizontal,
            )
        else:
            new_level_model = NewLevelLocationModel(system_model)
            model_unique_level = new_level_model.add_create_equipment_location_to_df(
                self.polygon_points_merge_control.layout_view_context_data.equipment_vertical
            )
        return model_unique_level

    def get_location_point_list(
            self, level_list_value: DynamicWidgetsViewContextData.level_list_value
    ) -> list:
        location_point_list = []
        for en, system in enumerate(self.polygon_points_merge_control.system_list):
            location_point = self.__create_equipment_location_point(system, level_list_value[en])
            location_point_list.append(location_point)
        return location_point_list
