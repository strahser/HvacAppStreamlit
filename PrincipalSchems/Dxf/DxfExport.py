import ezdxf
import pandas as pd
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
import streamlit as st

from PrincipalSchems.Controls.PlotterCreateLayout import PlotterCreateLayout

PLOTLY_COLORS = {
    'orange': 241,  # оранжевый
    'indigo': 6,  # темно-синий
    'lightpink': 211,  # светло-розовый
    'darkblue': 1,  # темно-синий (второй вариант)
    'firebrick': 1,  # красный кирпич (темно-красный)
    'orchid': 176,  # орхидея
    'yellowgreen': 142,  # желто-зеленый
    'goldenrod': 180,  # золотистый
    'blue': 5,  # синий
    'brown': 7,  # коричневый
    'red': 1,  # красный
    'coral': 210,  # коралловый
    'darkmagenta': 139,  # темно-пурпурный
    'green': 3,  # зеленый
    'cyan': 6,  # голубой
    'deeppink': 201,  # темно-розовый
}


class DxfExport:
    # Создаем новый чертеж
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    # Создаем слой для полигонов
    doc.layers.add('Polygons', color=colors.RED)  # Цвет слоя - 1 (красный)
    # Создаем слой для линий
    doc.layers.add('Lines', color=colors.BLUE)
    # Создаем слой для стрелок
    doc.layers.add('Arrows', color=colors.GREEN)

    text_layer = "TEXTLAYER"
    text_y_offset = 5

    def __init__(self, plotter_create_layout: PlotterCreateLayout):
        self.plotter_create_layout = plotter_create_layout
        self.polygon_points_merge_control = plotter_create_layout.polygon_plotter_merge_control
        self.location_point_list = plotter_create_layout.data_for_plotting.location_point_list
        self._df = self.polygon_points_merge_control.df_text._df
        self.level_property = self.polygon_points_merge_control.get_level_property()

    def save(self):
        self.doc.saveas("rectangles.dxf")

    def export_to_dxf_data(self):
        self.plot_space_polygons()
        self.plot_vertical_side_plot_lines_to_system()
        self.add_level_text()
        self.plot_start_end_system_lines()
        self._add_block_arrow()
        self.__plot_horizontal_line_to_equipment()
        self.save()

    def _add_block_arrow(self):
        if not self.doc.blocks.get('Arrow'):
            block = self.doc.blocks.new('Arrow')
            block.add_line(start=(0, 0), end=(0, 20), dxfattribs={'layer': 'Arrows'})  # Линия стрелки
            block.add_line(start=(0, 20), end=(-10, 10), dxfattribs={'layer': 'Arrows'})  # Левый наконечник
            block.add_line(start=(0, 20), end=(10, 10), dxfattribs={'layer': 'Arrows'})  # Правый наконечник

    def plot_space_polygons(self, show_color=True, line_color_filter=False):
        for idx, row in self._df.iterrows():
            line_color = row["color"] if show_color and line_color_filter else 'grey'
            self.msp.add_lwpolyline(
                points=[(x, y) for x, y in zip(row["px"], row["py"])],
                dxfattribs={"layer": 'Polygons', "color": PLOTLY_COLORS.get(line_color, 1)})
            if row["text"]:
                self.msp.add_text(
                    row["text"].replace('<br>', '\n').replace('None', ''),
                    dxfattribs={"layer": self.text_layer, "color": PLOTLY_COLORS.get(line_color, 1)}).set_placement(
                    (row["pcx"], row["pcy"]),
                    align=TextEntityAlignment.CENTER)

    def plot_vertical_side_plot_lines_to_system(self):
        """добовляем круги на пересечении этажей подъема оборудования"""
        for idx_, row in self.polygon_points_merge_control.add_color_df.iterrows():
            self.draw_circle(row["Max_x"], row["Max_y"], radius=1, fill_color=PLOTLY_COLORS.get(row['color'], 1))

    def add_level_text(self):
        """Название уровня на чертеже"""
        for prop in self.level_property:
            if prop.vertical_direction_list == "up" and prop.level_name:
                self.msp.add_text(
                    prop.level_name,
                    dxfattribs={"layer": self.text_layer}).set_placement(
                    (prop.level_coord_x, prop.level_coord_y),
                    align=TextEntityAlignment.CENTER
                )

    def plot_start_end_system_lines(self, textposition: str = "bottom left"):
        # from polygons up or down
        all_system_points = self.polygon_points_merge_control.system_property_points
        df_1 = pd.DataFrame([prop.__dict__ for prop in all_system_points]) \
            .groupby(['offset_point_x', 'offset_point_y'])["system_flow"].sum().reset_index()

        for point in all_system_points:
            # add flow
            self.msp.add_text(
                f"L={str(point.system_flow)}",
                dxfattribs={"layer": self.text_layer}).set_placement((point.x_start_points, point.y_start_points),
                                                                     align=TextEntityAlignment.CENTER)
            arrow_name = ezdxf.ARROWS.closed_filled
            self.msp.add_arrow(name=arrow_name,
                               size=5,
                               rotation=-90,  # down
                               insert=(point.x_start_points, point.y_start_points),
                               dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})
            # add offset sum flow
            for idx, row in df_1.iterrows():
                if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
                    level_text = f"{point.level_value} L{point.system_name} = {round(row['system_flow'])}"
                    self.msp.add_text(
                        level_text,
                        dxfattribs={"layer": self.text_layer}).set_placement(
                        (point.offset_point_x, point.offset_point_y),
                        align=TextEntityAlignment.LEFT)
            # from polygons up or down
            self.msp.add_line(
                start=(point.x_start_points, point.y_start_points),
                end=(point.x_end_points, point.y_end_points),
                dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})
            # offset points
            offset_start = (point.x_end_points, point.y_end_points)
            offset_end = (point.offset_point_x, point.offset_point_y)
            self.msp.add_line(
                start=offset_start,
                end=offset_end,
                dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})
            # add system name for  offset points
            text_system_name = point.system_name
            self.msp.add_text(
                text_system_name,
                dxfattribs={"layer": self.text_layer}).set_placement(self.midpoint(offset_start, offset_end),
                                                                     align=TextEntityAlignment.CENTER)

    def __add_equipment_text(self, row, en):
        text_coordinates = (row["base_point_x"], row["base_point_y"])
        text = row["system_name"] \
               + row[self.polygon_points_merge_control.layout_view_context_data.level_column] \
               + str(
            self.plotter_create_layout.data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]
        )
        self.msp.add_text(
            text,
            dxfattribs={"layer": self.text_layer}).set_placement(
            text_coordinates,
            align=TextEntityAlignment.CENTER)

    def __add_equipment_marker(self, row, en):
        text = self.plotter_create_layout.data_for_plotting.dynamic_widgets_view_context_data.equipment_symbol_list[en]
        text_coordinates = (row["base_point_x"], row["base_point_y"])
        self.msp.add_text(
            text,
            dxfattribs={"layer": self.text_layer}).set_placement(
            text_coordinates,
            align=TextEntityAlignment.CENTER)

    def __plot_horizontal_line_to_equipment(self):
        """Доводим горизонтальюную линюю смещения до точки расположения оборудования"""
        for en, df in enumerate(self.location_point_list):  # levels iteration
            for idx_, row in df.iterrows():  # df row iteration
                # from polygons up or down
                x = [row["base_point_x"], row["px"]],
                y = [row["base_point_y"], row["py"]],
                for x1, y1 in zip(x, y):
                    self.msp.add_line(
                        start=(x1[0], y1[0]),
                        end=(x1[1], y1[1]),
                        dxfattribs={"color": PLOTLY_COLORS.get(row["color"], 1)})
                self.__add_equipment_marker(row, en)

    @staticmethod
    def midpoint(point1, point2):
        """
        Функция для определения середины отрезка.

        Args:
          point1: Первая точка отрезка (кортеж из двух координат).
          point2: Вторая точка отрезка (кортеж из двух координат).

        Returns:
          Кортеж из двух координат, представляющий середину отрезка.
        """
        x_mid = (point1[0] + point2[0]) / 2
        y_mid = (point1[1] + point2[1]) / 2
        return (x_mid, y_mid)

    def draw_circle(self, center_x, center_y, radius, fill_color=7):
        """
        Рисует окружность с заливкой.

        Args:
            center_x: Координата X центра окружности.
            center_y: Координата Y центра окружности.
            radius: Радиус окружности.
            fill_color: Цвет заливки (по умолчанию - коричневый, 7).
        """
        circle = self.msp.add_circle(center=(center_x, center_y), radius=radius, dxfattribs={'layer': 'Circles'})
        circle.dxf.extrusion = (0, 0, 1)  # Устанавливаем направление экструзии для заливки
        circle.dxf.color = fill_color  # Устанавливаем цвет заливки
