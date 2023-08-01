from PrincipalSchems.View.DynamicBaseView import *


class DynamicSystemView(DynamicBaseView):

    def __init__(self, df_: pd.DataFrame,key, columns_number: int = 10) -> None:
        super().__init__(df_,key, columns_number)

    def add_distance_widget_to_df(self, column_number=2, system_distance=60):
        start_position = 0
        self.columns[column_number].write("Start distance")
        for ind, row in self.df_.iterrows():
            setattr(
                self,
                f"distance_{row['system']}",
                self.columns[column_number].number_input(
                    "#",
                    start_position + system_distance,
                    key=f'{self.key} distance_{row["system"]}',
                    label_visibility="collapsed",
                ),
            )
            start_position += system_distance

    def add_color_widget_to_df(
        self,
        config: MainSchemeConfig,
        column_number=3,
        color_revers =False
    ):
        if color_revers:
            revised_list = config.colors[::-1]
            color_circle = cycle(revised_list)
        else:
            color_circle = cycle(config.colors)
        self.columns[column_number].write("Select color")
        for ind, row in self.df_.iterrows():
            setattr(
                self,
                f"color_{row['system']}",
                self.columns[column_number].selectbox(
                    "#",
                    config.colors,
                    key=f"{self.key} color_" + row["system"],
                    index=config.colors.index(str(next(color_circle))),
                    label_visibility="collapsed",
                ),
            )

    def add_system_vertical_direction(self, column_number=4):
        """option to excitation"""
        self.columns[column_number].write("Vertical Direction")
        for ind, row in self.df_.iterrows():
            setattr(
                self,
                f"vertical_direction_{row['system']}",
                self.columns[column_number].selectbox(
                    "#",
                    MainSchemeConfig.vertical_direction_list,
                    key=f"{self.key} vertical_direction" + row["system"],
                    label_visibility="collapsed",
                ),
            )

    def add_system_horizontal_direction(self, column_number=4):
        """option to excitation"""
        self.columns[column_number].write("Horizontal Direction")
        for ind, row in self.df_.iterrows():
            setattr(
                self,
                f"horizontal_direction_{row['system']}",
                self.columns[column_number].selectbox(
                    "#",
                    MainSchemeConfig.horizontal_direction_list,
                    key=f"{self.key} horizontal_direction" + row["system"],
                    label_visibility="collapsed",
                ),
            )