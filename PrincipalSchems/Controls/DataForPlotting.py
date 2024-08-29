import pandas as pd

from PrincipalSchems.Controls.EquipmentPointLocationControl import EquipmentPointLocationControl
from PrincipalSchems.Controls.PolygonPointsMergeControl import PolygonPointsMergeControl
from PrincipalSchems.View.MainLayoutView import DynamicLayoutViewContextData, TabsView, DynamicWidgetsViewContextData


class DataForPlotting:
    def __init__(self, input_df: pd.DataFrame, tab: TabsView):
        self.dynamic_layout_context_data = DynamicLayoutViewContextData(
            tab.dynamic_layout
        )

        self.dynamic_widgets_view_context_data = DynamicWidgetsViewContextData(
            self.dynamic_layout_context_data
        )
        self.polygon_points_merge_control = PolygonPointsMergeControl(input_df, tab)
        self.polygon_points_merge_control.calculate()
        self.equipment_location = EquipmentPointLocationControl(
            self.polygon_points_merge_control
        )
        self.location_point_list = self.equipment_location.get_location_point_list(
            self.dynamic_widgets_view_context_data.level_list_value
        )
        self.plot_title = tab.static_layout.plot_title
