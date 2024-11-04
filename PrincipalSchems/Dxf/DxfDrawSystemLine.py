import ezdxf
from ezdxf.enums import TextEntityAlignment
import pandas as pd
from PrincipalSchems.Dxf.DxfDocument import DxfDocument
from PrincipalSchems.Models.ConstantModel import SystemProperty
from PrincipalSchems.Dxf.DxfConstants import TEXT_PROPERTY, PLOTLY_COLORS, ARROW_SIZE


def plot_vertical_side_plot_lines_to_system(msp, color_df: pd.DataFrame):
    """"color_df data_for_plotting.polygon_points_merge_control.add_color_df"""
    # between levels
    for idx_, row in color_df.iterrows():
        msp.add_line(
            start=(row["Max_x"], row["Max_y"]),
            end=(row["Min_x"], row["Min_y"]),
            dxfattribs={'layer': row["system_name"]})


class DxfDrawSystemLine:
    def __init__(self, point: SystemProperty):
        self.doc = DxfDocument.doc
        self.msp = DxfDocument.msp
        self.point = point
        self.offset_start = (self.point.x_end_points, self.point.y_end_points)
        self.offset_end = (self.point.offset_point_x, self.point.offset_point_y)

    def draw_lines_and_schem_text(self):
        self.__create_system_name_layer()
        self.__add_vertical_line_from_polygons()
        self.__add_arrow_line_to_space()
        # self.__add_horizontal_system_lines_to_level_point()
        self.__add_system_flow_to_space()

    def __create_system_name_layer(self):
        if self.point.system_name not in self.doc.layers:
            self.doc.layers.add(self.point.system_name, color=PLOTLY_COLORS.get(self.point.color, 1))

    def __add_vertical_line_from_polygons(self):
        """из каждого помещения добавляет линию"""
        self.msp.add_line(
            start=(self.point.x_start_points, self.point.y_start_points),
            end=(self.point.x_end_points, self.point.y_end_points),
            dxfattribs={'layer': self.point.system_name})

    def __add_arrow_line_to_space(self):
        arrow_name = ezdxf.ARROWS.closed_filled
        self.msp.add_arrow(name=arrow_name,
                           size=ARROW_SIZE,
                           rotation=-90,  # down
                           insert=(self.point.x_start_points, self.point.y_start_points),
                           dxfattribs={"color": PLOTLY_COLORS.get(self.point.color, 1)})

    def __add_horizontal_system_lines_to_level_point(self):
        self.msp.add_line(
            start=self.offset_start,
            end=self.offset_end,
            dxfattribs={'layer': self.point.system_name})

    def __add_level_flow(self, system_flow: float):
        """"Отрисовывает текст в точке подключения уровня offset_point"""
        level_text = f"{self.point.level_value} {self.point.system_name} L = {round(system_flow)}"
        level_points = (self.point.offset_point_x, self.point.offset_point_y)
        self.msp.add_text(
            level_text,
            dxfattribs=TEXT_PROPERTY).set_placement(level_points, align=TextEntityAlignment.LEFT)

    def __add_system_flow_to_space(self) -> None:
        _text = f"{self.point.system_name}\n L={str(self.point.system_flow)}"
        mtext = self.msp.add_mtext(_text, dxfattribs=TEXT_PROPERTY)
        mtext.dxf.insert = (self.point.x_start_points + 5, self.point.y_start_points + 10)

    @staticmethod
    def __midpoint(point1, point2) -> tuple[float, float]:
        x_mid = (point1[0] + point2[0]) / 2
        y_mid = (point1[1] + point2[1]) / 2
        return x_mid, y_mid

    def __add_system_name_text_to_middle_of_line(self):
        # add system name for  offset points
        self.msp.add_text(
            self.point.system_name,
            dxfattribs=TEXT_PROPERTY).set_placement(self.__midpoint(self.offset_start, self.offset_end),
                                                    align=TextEntityAlignment.CENTER)
