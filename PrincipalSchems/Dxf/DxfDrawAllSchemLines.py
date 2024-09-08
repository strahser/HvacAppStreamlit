import pandas as pd
import streamlit
from ezdxf.enums import TextEntityAlignment

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Dxf.DxfConstants import TEXT_PROPERTY, TEXT_LEVEL_FLOW_OFFSET
from PrincipalSchems.Dxf.DxfDocument import DxfDocument
from PrincipalSchems.Dxf.DxfDrawSystemLine import DxfDrawSystemLine


class DxfDrawAllSchemLines:
    def __init__(self, data_for_plotting: DataForPlotting):
        self.data_for_plotting = data_for_plotting
        self.system_points_list = data_for_plotting.polygon_points_merge_control.system_property_points
        self.level_system_point_group_df = pd.DataFrame([prop.__dict__ for prop in self.system_points_list]) \
            .groupby(['system_name', 'offset_point_x', 'offset_point_y'])["system_flow"] \
            .sum().reset_index()
        self.legend_system_df = pd.DataFrame([prop.__dict__ for prop in self.system_points_list]) \
            .groupby(['system_name'])["system_flow"].sum().reset_index()
        self.msp = DxfDocument.msp

    def __add_horizontal_system_lines_to_level_point(self) -> None:
        p_list = []
        for point in self.system_points_list:
            point.level_distance = point.calculate_distance()
            p_list.append(point)
        all_df = pd.DataFrame(p_list)
        level_df = pd.DataFrame(p_list) \
            .groupby(['system_name', 'level_value'])['level_distance'] \
            .max().reset_index()
        result = pd.merge(level_df, all_df, on=['system_name', 'level_value', 'level_distance'], how='left')
        for idx, row in result.iterrows():
            self.msp.add_line(
                start=(row['x_end_points'], row['y_end_points']),
                end=(row['offset_point_x'], row['offset_point_y']),
                dxfattribs={'layer': row['system_name']})

    def plot_start_end_system_lines(self):
        self.__add_horizontal_system_lines_to_level_point()
        for point in self.system_points_list:
            system_line = DxfDrawSystemLine(point)
            system_line.draw_lines_and_schem_text()

    def draw_legend(self, start_block_coordinates=0):
        start_x = 1000
        start_y = 1000 + start_block_coordinates
        increment = 0
        line_length = 20

        for idx, row in self.legend_system_df.iterrows():
            self.msp.add_line(start=(start_x, start_y + increment), end=(start_x + line_length, start_y + increment),
                              dxfattribs={'layer': row["system_name"]})

            self.msp.add_text(row["system_name"], dxfattribs=TEXT_PROPERTY) \
                .set_placement((start_x + line_length + 5, start_y + increment),
                               align=TextEntityAlignment.LEFT)
            increment += 20

        return increment

    def add_level_flow_(self):
        """"Отрисовывает текст в точке подключения уровня offset_point"""

        for idx, row in self.level_system_point_group_df.iterrows():
            level_points = (
            row['offset_point_x'] + TEXT_LEVEL_FLOW_OFFSET, row['offset_point_y'] + TEXT_LEVEL_FLOW_OFFSET)
            level_text = f"Система {row['system_name']} Расход {round(row['system_flow'])}"
            self.msp.add_text(
                level_text,
                dxfattribs=TEXT_PROPERTY).set_placement(level_points,
                                                        align=TextEntityAlignment.LEFT)
