from PrincipalSchems.View.DynamicEquipmentPropertyView import *
from PrincipalSchems.View.DynamicSystemView import *
from PrincipalSchems.View.PlotConfigView import *
from PrincipalSchems.View.SystemAndFlowView import *
from PrincipalSchems.View.LevelView import *
from PrincipalSchems.View.SpaceView import *
from Utility.SystemGroupCreator import *
from StaticData.AppConfig import MenuChapters


class SpacePlotView:
    def __init__(self, revit_df: pd.DataFrame, key) -> None:
        self.revit_df = revit_df
        self.color_filter_name = st.selectbox("select color filter column", self.revit_df.columns,
                                              key=f"{key} color_filter_name")
        self.space_value = st.multiselect("select space input data column", self.revit_df.columns,
                                          key=f"{key} space_value")
        self.space_prefix = st.text_input("select prefix", key=f"{key} space_prefix")
        self.space_suffix = st.text_input("select suffix", key=f"{key} space_suffix")


class StaticLayoutView:
    def __init__(self, df_: pd.DataFrame, key) -> None:
        """create level column,plote config space config property

        Args:
            df_ (pd.DataFrame): _description_
        """
        self.key = key
        self.columns = st.columns(3)
        self.df_ = df_
        self.columns[0].subheader("Select Columns")
        self.plot_title = self.columns[0].text_input(
            "Type Plot Title", value="Plot Title"
        )
        self.ID_COLUMN = self.columns[0].selectbox("Select ID column", self.df_.columns)

    def _choose_level_column(self):
        with self.columns[0]:
            self.level_view_choose_column = LevelView(self.df_, key=self.key)
            self.level_view_choose_column.choose_level_column()
            self.level_column_value = ["S_ID", self.level_view_choose_column.level_column]  # todo change SID

    def _add_plot_config(self):
        self.plot_config = PlotConfigView(key=self.key)
        self.plot_config.add_plot_size()
        self.color_view_checkbox = st.checkbox("add color to space?", value=True, key=self.key)
        self.space_data_view = SpacePlotView(self.df_, key=self.key)

    def _add_space_dimensions(self):
        self.space_dimension_view = SpaceDimensionView(key=self.key)
        self.space_dimension_view.add_polygon_config_widget()


class SystemAndFlowLayoutView:
    def __init__(self, static_layout: StaticLayoutView, uniq_key) -> None:
        """join static  views. For tabs layouts."""
        self.system_and_flow_view = None
        self.df_ = static_layout.df_
        self.static_layout = static_layout
        self.columns = static_layout.columns
        self.uniq_key = uniq_key

    def _waring_if_main_data_not_load(self):
        return st.warning("please set system columns and  flow and level columns ")

    def create_system_and_flow_view_instance(self):
        """add level and id column"""
        self.system_and_flow_view = SystemAndFlowView(self.df_, f"SystemAndFlowView {self.uniq_key}"
                                                      )

    def get_layout_system_property(self, column_number=1, subhider=""):
        """create unique key for main layout

        Args:
            column_number (int, optional): _description_. Defaults to 1.
            sub-hider (str, optional): _description_. Defaults to "".
        """
        with self.columns[column_number]:
            st.subheader(f"System Property {subhider}")
            self.system_and_flow_view.add_system_data_to_view()
        self.main_columns = (
                ["S_ID"]
                + self.system_and_flow_view.system_columns
                + self.system_and_flow_view.flow_columns
        )

    def _is_input_data_load(self):
        flow_condition = len(self.system_and_flow_view.system_columns) == len(
            self.system_and_flow_view.flow_columns
        )
        return (
                flow_condition
                and self.system_and_flow_view.system_columns
                and self.static_layout.level_view_choose_column.level_column
        )


class DynamicLayoutView:
    def __init__(self, system_and_flow_view: SystemAndFlowLayoutView, key, columns_number) -> None:
        """create equipment dynamic system dynamic property
        """
        self.key = key
        self.static_layout = system_and_flow_view.static_layout
        self.df_ = system_and_flow_view.static_layout.df_
        self.system_and_flow_view = system_and_flow_view
        self.unique_sys = self._create_unique_system_flow_groups()
        self.columns_number = columns_number

    def _create_equipment_dynamic_layout(self):
        self.level_view = DynamicEquipmentPropertyView(self.unique_sys, key=self.key, columns_number=6)
        self.level_view.add_system_widget_to_df(0, 1)
        self.level_view._equipment_config_add_label_to_layout()
        self.level_view.add_level_widget_to_layout(
            self.df_[self.static_layout.level_view_choose_column.level_column].unique(), 1)
        self.level_view.add_flow_widget_to_layout(2)
        self.level_view.add_symbol_widget_to_layout(3)

    def _create_system_property_dynamic_layout(
            self, color_revers: bool = False, system_distance=60
    ):
        self.system_view = DynamicSystemView(self.unique_sys, 5)
        self.system_view.add_system_widget_to_df(0)
        self.system_view.add_distance_widget_to_df(1, system_distance)
        self.system_view.add_color_widget_to_df(MainSchemeConfig, 2, color_revers)

    def _create_unique_system_flow_groups(self) -> pd.DataFrame:
        unique_sys = get_system_flow_groups(
            self.system_and_flow_view.df_,
            self.system_and_flow_view.system_and_flow_view.system_columns,
            self.system_and_flow_view.system_and_flow_view.flow_columns,
        )
        return unique_sys


class TabsView:
    def __init__(self, static_layout_view: StaticLayoutView, key, color_reverse: bool = False):
        self.static_layout = static_layout_view
        self.color_reverse = color_reverse
        self.key = key

    def is_input_data_load(self):
        return self.system_and_flow_view._is_input_data_load()

    def waring_if_main_data_not_load(self):
        self.system_and_flow_view._waring_if_main_data_not_load()

    def create_choose_column_level(self):
        self.static_layout._choose_level_column()

    def create_choose_system_property(self, column_number: int = 1, subhider: str = "", uniq_key=""):
        self.system_and_flow_view = SystemAndFlowLayoutView(self.static_layout, uniq_key=uniq_key)
        self.system_and_flow_view.create_system_and_flow_view_instance()
        self.system_and_flow_view.get_layout_system_property(column_number, subhider)

    def create_space_dimensions(self):
        self.static_layout._add_space_dimensions()

    def add_plot_config(self):
        self.static_layout._add_plot_config()

    def create_dynamic_equipment_layout(self):
        self.dynamic_layout = DynamicLayoutView(self.system_and_flow_view, key=self.key, columns_number=10)
        self.dynamic_layout._create_equipment_dynamic_layout()

    def create_dynamic_system_layout(self):
        self.layout_view_context_data = LayoutViewContextData(
            self.system_and_flow_view, self.static_layout
        )
        self.dynamic_layout._create_system_property_dynamic_layout(
            self.color_reverse,
            system_distance=self.static_layout.space_dimension_view.distance_between_systems,
        )


# endregion

# region Context Data


class LayoutViewContextData:
    def __init__(self, system_and_flow_layout_view: SystemAndFlowLayoutView, static_layout: StaticLayoutView):
        """get call back from layout static wigets

        Args:
            system_and_flow_layout_view (SystemAndFlowLayoutView): _description_
            static_layout (StaticLayoutView): _description_
        """
        self.ID = static_layout.ID_COLUMN
        self.plot_title = static_layout.plot_title
        self.level_distance: int = static_layout.space_dimension_view.level_distance
        self.polygon_width: int = static_layout.space_dimension_view.polygon_width
        self.polygon_height: int = static_layout.space_dimension_view.polygon_height
        self.color_view_checkbox: bool = static_layout.color_view_checkbox
        self.equipment_horizontal: int = (
            system_and_flow_layout_view.static_layout.space_dimension_view.equipment_distance_horizontal
        )
        self.equipment_vertical: int = system_and_flow_layout_view.static_layout.space_dimension_view.equipment_distance_vertical

        self.distance_between_systems: int = static_layout.space_dimension_view.distance_between_systems
        self.plot_height: float = static_layout.plot_config.plot_height
        self.plot_width: float = static_layout.plot_config.plot_width
        self.level_column: str = static_layout.level_view_choose_column.level_column
        self.space_data_view: SpacePlotView = static_layout.space_data_view
        self.vertical_direction_list: str = system_and_flow_layout_view.system_and_flow_view.vertical_direction_list
        self.horizontal_direction_list: str = system_and_flow_layout_view.system_and_flow_view.horizontal_direction_list

        self.main_columns: list = system_and_flow_layout_view.main_columns
        self.system_columns: list[str] = system_and_flow_layout_view.system_and_flow_view.system_columns
        self.flow_columns: list[str] = system_and_flow_layout_view.system_and_flow_view.flow_columns


class DynamicLayoutViewContextData:
    def __init__(self, dynamic_layout_view: DynamicLayoutView) -> None:
        """system,flow,line direction"""
        self.base_property_widget = dynamic_layout_view.system_view
        # distance,color
        self.level_property_widget = dynamic_layout_view.level_view
        # system and flow
        self.unique_systems: pd.DataFrame = dynamic_layout_view.unique_sys


class DynamicWidgetsViewContextData:
    def __init__(self, dynamic_layout_context_data: DynamicLayoutViewContextData) -> None:
        """equipment level,symbol"""
        self.dynamic_layout_context_data = dynamic_layout_context_data
    @property
    def level_list_value (self):
        level_list_value = [
            getattr(
                self.dynamic_layout_context_data.level_property_widget,
                f"level_label_{val}",
            )
            for val in self.dynamic_layout_context_data.unique_systems["system"]
        ]
        return level_list_value

    @property
    def flow_list_value(self):
        flow_list_value = [
            getattr(
                self.dynamic_layout_context_data.level_property_widget,
                f"flow_label_{val}",
            )
            for val in self.dynamic_layout_context_data.unique_systems["system"]
        ]
        return flow_list_value

    @property
    def equipment_symbol_list(self):
        equipment_symbol_list = [
            getattr(
                self.dynamic_layout_context_data.level_property_widget,
                f"equipment_symbol_{val}",
            )
            for val in self.dynamic_layout_context_data.unique_systems["system"]
        ]

        return equipment_symbol_list

    @property
    def legend_group(self):
        legend_group = [
            getattr(
                self.dynamic_layout_context_data.level_property_widget,
                f"equipment_label_{val}",
            )
            for val in self.dynamic_layout_context_data.unique_systems["system"]
        ]
        return legend_group
# endregion
