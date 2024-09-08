import pandas as pd

from PrincipalSchems.Models.ConstantModel import SystemProperty
from PrincipalSchems.View.DynamicSystemView import DynamicSystemView
from PrincipalSchems.View.MainLayoutView import TabsView


class WidgetsModelControl:
    """
    StaticData class. Add distance and color to SystemProperty from widgets.
    """

    @staticmethod
    def add_start_widget_property(
            dict_df: dict,
            widget_instance: DynamicSystemView,
    ) -> list[SystemProperty]:
        """add distance and color to instance

        Args:
            dict_df (dict): _description_
            widget_instance (DynamicSystemView): _description_

        Returns:
            _type_: _description_
        """
        dict_df_ = dict_df.copy()
        sys_prop = []

        for key, val in dict_df.items():
            start_list = {}
            for val_id in val:
                if val_id:
                    sys_property = SystemProperty()
                    sys_property.space_id = key
                    sys_property.system_name = val_id
                    sys_property.distance_to_line = getattr(
                        widget_instance, f"distance_{val_id}"
                    )
                    sys_property.color = getattr(widget_instance, f"color_{val_id}")
                    start_list.update({val_id: sys_property})
                    dict_df_[key] = start_list
                    sys_prop.append(sys_property)
        return sys_prop

    @staticmethod
    def add_color_to_widget(widget_instance, sys_name):
        return getattr(widget_instance, f"color_{sys_name}")

    @staticmethod
    def create_and_add_property_to_system_property(input_df: pd.DataFrame, tabs_view1: TabsView):
        """
        create SystemProperty and add
        """
        flow_columns = tabs_view1.system_and_flow_view.system_and_flow_view.flow_columns
        system_columns = tabs_view1.system_and_flow_view.system_and_flow_view.system_columns
        level_column = tabs_view1.static_layout.level_view_choose_column.level_column
        input_df = input_df.fillna(0)
        system_property_list: list[SystemProperty] = []
        wiget_instance = tabs_view1.dynamic_layout.system_view
        for flow, sys_name in zip(flow_columns, system_columns):
            for idx, row in input_df.iterrows():
                # add main property from input df
                sys_prop = SystemProperty()
                sys_prop.system_flow = row[flow]
                sys_prop.system_name = row[sys_name]
                sys_prop.space_id = row["S_ID"]
                sys_prop.level_value = row[level_column]
                # add color and distatnce
                if sys_prop.system_name != 0:
                    sys_prop.distance_to_line = getattr(
                        wiget_instance, f"distance_{sys_prop.system_name}"
                    )
                    sys_prop.color = getattr(
                        wiget_instance, f"color_{sys_prop.system_name}"
                    )
                    sys_prop.vertical_direction_list = (
                        tabs_view1.layout_view_context_data.vertical_direction_list
                    )
                    sys_prop.horizontal_direction_list = (
                        tabs_view1.layout_view_context_data.horizontal_direction_list
                    )
                    system_property_list.append(sys_prop)
        return system_property_list

    @staticmethod
    def make_widget_group(input_df: pd.DataFrame, tabs_view1: TabsView):
        widget_instance = tabs_view1.dynamic_layout.system_view
        system_property_list = (
            widget_instance.create_and_add_propertys_to_system_property(
                input_df, tabs_view1
            )
        )
        # create df for grouping.
        df_widgets = pd.DataFrame({"wigets": system_property_list})
        df_widgets["space_id"] = df_widgets["wigets"].apply(lambda x: x.space_id)
        df_widgets = df_widgets.groupby("space_id")["wigets"].apply(list).reset_index()
        return df_widgets
