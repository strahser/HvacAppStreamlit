import sys

import matplotlib.pyplot as plt
import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
from ezdxf.lldxf import const as dxf_const
import pandas as pd
import streamlit as st

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
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
    'blue': colors.BLUE,  # синий
    'brown': 7,  # коричневый
    'red': 1,  # красный
    'coral': 210,  # коралловый
    'darkmagenta': 139,  # темно-пурпурный
    'green': 3,  # зеленый
    'cyan': 6,  # голубой
    'deeppink': 201,  # темно-розовый
}
TEXT_PROPERTY = {'style': "ISOCPEUR", "layer": "TEXTLAYER"}


class DxfBlockCreator:
    def __init__(self, doc, supply_air_block_name, block_layer):
        self.doc = doc
        self.supply_air_block_name = supply_air_block_name
        self.block_layer = block_layer

    def create_supply_unit_block(self, width=10, height=5):
        """
        Создает блок условного обозначения приточной установки в DXF-чертеже.

        Args:
            width: Ширина блока.
            height: Высота блока.
        """

        block = self.doc.blocks.new(name=self.supply_air_block_name)

        section_width = width / 3

        # Рисуем прямоугольник
        block.add_lwpolyline(points=[
            (0, 0),
            (width, 0),
            (width, height),
            (0, height),
            (0, 0)
        ], dxfattribs={'layer': self.block_layer})

        # Разделяем прямоугольник на секции
        for i in range(1, 3):
            block.add_line(start=(i * section_width, 0), end=(i * section_width, height),
                           dxfattribs={'layer': self.block_layer})

        # Рисуем вентилятор
        block.add_circle(center=(section_width / 2, height / 2), radius=height / 4,
                         dxfattribs={'layer': self.block_layer})
        block.add_line(start=(section_width / 4, height / 2), end=(3 * section_width / 4, height / 2),
                       dxfattribs={'layer': self.block_layer})

        # Рисуем теплообменник
        block.add_text(text="+",
                       dxfattribs={'layer': self.block_layer}).set_placement(
            (section_width * 1.5, height / 2), align=TextEntityAlignment.CENTER)
        block.add_text(text="-",
                       dxfattribs={'layer': self.block_layer}).set_placement(
            (
                (section_width * 1.5, height / 3)),
            align=TextEntityAlignment.CENTER)

        # Рисуем фильтр
        block.add_polyline2d(points=[
            (section_width * 2.25, height / 4),
            (section_width * 2.75, height / 4),
            (section_width * 2.75, 3 * height / 4),
            (section_width * 2.25, 3 * height / 4),
            (section_width * 2.25, height / 4)
        ], dxfattribs={'layer': self.block_layer})


class DxfExport:
    # Создаем новый чертеж
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    # Создаем слой для полигонов
    doc.layers.add('Polygons', color=colors.RED)  # Цвет слоя - 1 (красный)
    doc.layers.add('supply_air_layer', color=colors.BLUE)
    supply_air_block_name = 'supply_air_unit'
    doc_name = "rectangles.dxf"
    text_y_offset = 5

    def __init__(self, data_for_plotting: list[DataForPlotting]):
        self.data_for_plotting = data_for_plotting
        # polygon_points_merge_control_0 Для  полигонов, надписи уровня
        self.polygon_points_merge_control_0 = data_for_plotting[0].polygon_points_merge_control

    @property
    def level_property(self):
        """ level_property Надпись уровня на чертеже"""
        return self.polygon_points_merge_control_0.get_level_property()

    @property
    def text_worker_df(self):
        """text_worker_df  Таблица с текстом полигона  px,py,pcx,pcy,color"""
        return self.polygon_points_merge_control_0.text_worker.df

    def save(self):
        self.doc.saveas(self.doc_name)

    def export_to_dxf_data(self):
        if not self.doc.blocks.get(self.supply_air_block_name):
            creator = DxfBlockCreator(self.doc, self.supply_air_block_name, 'supply_air_layer')
            creator.create_supply_unit_block()
        self.plot_space_polygons_and_text()
        self.add_level_text()
        all_data = []
        start_point = [2000, 500]
        increment = 20
        for data in self.data_for_plotting:
            data_system = self.plot_start_end_system_lines(data)
            all_data.extend(data_system)
            self.__plot_horizontal_line_to_equipment(data)
        all_data = sorted(all_data)
        for data in all_data:
            self.msp.add_line(
                start=(start_point[0], start_point[1]),
                end=(start_point[0] + 100, start_point[1]),
                dxfattribs={"color": PLOTLY_COLORS.get(data[1], 1)})
            self.msp.add_text(
                data[0],
                dxfattribs=TEXT_PROPERTY).set_placement((start_point[0] + 120, start_point[1]),
                                                        align=TextEntityAlignment.LEFT)
            start_point[1] -= increment

        self.save()
        # self.export_to_mpl()

    def plot_space_polygons_and_text(self, show_color=True, line_color_filter=True):
        """ Обрисовывает полигон и текст"""
        for idx, row in self.text_worker_df.iterrows():
            line_color = row["color"] if show_color and line_color_filter else 'grey'
            self.msp.add_lwpolyline(
                points=[(x, y) for x, y in zip(row["px"], row["py"])],
                dxfattribs={"layer": 'Polygons', "color": PLOTLY_COLORS.get(line_color, colors.GRAY)})
            if row["text"]:
                _text = row["text"].replace('<br>', '\n').replace('None', 'Нет')
                self.msp.add_mtext(_text, dxfattribs=TEXT_PROPERTY) \
                    .dxf.insert = (row["pcx"] - 20, row["pcy"] + 20, 0)

    def add_level_text(self):
        """Название уровня на чертеже"""
        for prop in self.level_property:
            self.msp.add_text(
                prop.level_name,
                dxfattribs=TEXT_PROPERTY).set_placement(
                (prop.level_coord_x, prop.level_coord_y),
                align=TextEntityAlignment.CENTER
            )

    def plot_start_end_system_lines(self, data_for_plotting: DataForPlotting) -> set[tuple[str, str]]:
        def __add_system_flow_and_arrow_to_space() -> None:
            _text = f" {point.system_name}\n L={str(point.system_flow)}"
            mtext = self.msp.add_mtext(_text, dxfattribs=TEXT_PROPERTY)
            mtext.dxf.insert = (point.x_start_points + 5, point.y_start_points + 20)
            arrow_name = ezdxf.ARROWS.closed_filled
            self.msp.add_arrow(name=arrow_name,
                               size=5,
                               rotation=-90,  # down
                               insert=(point.x_start_points, point.y_start_points),
                               dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})

        def __add_level_flow_():
            """"Отрисовывает текст в точке подключения уровня offset_point"""

            def add_system_name_text():
                self.msp.add_text(
                    level_text,
                    dxfattribs=TEXT_PROPERTY).set_placement(level_points,
                                                            align=TextEntityAlignment.LEFT)

            for idx, row in df_1.iterrows():
                if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
                    level_points = (point.offset_point_x, point.offset_point_y)
                    level_text = f"{point.level_value} {point.system_name}L = {round(row['system_flow'])}"
                    add_system_name_text()

        def __add_vertical_line_from_polygons():
            """из каждого помещения добавляет линию"""
            self.msp.add_line(
                start=(point.x_start_points, point.y_start_points),
                end=(point.x_end_points, point.y_end_points),
                dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})

        def __add_horizontal_system_lines_to_level_point():
            def midpoint(point1, point2):
                x_mid = (point1[0] + point2[0]) / 2
                y_mid = (point1[1] + point2[1]) / 2
                return x_mid, y_mid

            def add_system_name_text():
                # add system name for  offset points
                self.msp.add_text(
                    point.system_name,
                    dxfattribs=TEXT_PROPERTY).set_placement(midpoint(offset_start, offset_end),
                                                            align=TextEntityAlignment.CENTER)

            offset_start = (point.x_end_points, point.y_end_points)
            offset_end = (point.offset_point_x, point.offset_point_y)
            self.msp.add_line(
                start=offset_start,
                end=offset_end,
                dxfattribs={"color": PLOTLY_COLORS.get(point.color, 1)})

        _system_points = data_for_plotting.polygon_points_merge_control.system_property_points
        # группируем и получаем  по системам в каждой точке offset_point   "system_flow"
        df_1 = pd.DataFrame([prop.__dict__ for prop in _system_points]) \
            .groupby(['offset_point_x', 'offset_point_y'])["system_flow"] \
            .sum().reset_index()
        unique_points = set()
        for point in _system_points:
            __add_system_flow_and_arrow_to_space()  # add flow
            __add_level_flow_()  # add offset sum flow
            __add_vertical_line_from_polygons()  # from polygons up or down
            __add_horizontal_system_lines_to_level_point()
            unique_points.add((point.system_name, point.color))
        return unique_points

    def insert_supply_unit_block(self, block_layer: str, text_coordinates: tuple[float, float], system_name: str):
        def __add_attrib():
            blockref.add_attrib(tag='system_name', text=system_name, dxfattribs={'invisible': False, 'height': 2, }) \
                .set_placement((text_coordinates[0], text_coordinates[1] + 12))

        blockref = self.msp.add_blockref(name=self.supply_air_block_name, insert=text_coordinates,
                                         dxfattribs={'layer': block_layer,
                                                     'xscale': 2,
                                                     'yscale': 2},
                                         )
        self.msp.add_text(
            system_name,
            dxfattribs=TEXT_PROPERTY).set_placement(
            (text_coordinates[0], text_coordinates[1] + 12),
            align=TextEntityAlignment.CENTER
        )

    def __add_equipment_marker(self, row, en, data_for_plotting: DataForPlotting):
        def __get_equipment_text():
            level_text = row[data_for_plotting.polygon_points_merge_control.layout_view_context_data.level_column]
            system_flow = data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]
            text = f"{row['system_name']} {system_flow}"
            return text

        # equipment_symbol = self.data_for_plotting[0].dynamic_widgets_view_context_data.equipment_symbol_list[en]
        text_coordinates = (row["base_point_x"], row["base_point_y"])
        self.insert_supply_unit_block(self.supply_air_block_name,
                                      text_coordinates,
                                      system_name=__get_equipment_text())

    def __plot_horizontal_line_to_equipment(self, data_for_plotting: DataForPlotting):
        """Доводим горизонтальюную линюю смещения до точки расположения оборудования"""
        for en, df in enumerate(data_for_plotting.location_point_list):  # levels iteration
            for idx_, row in df.iterrows():  # df row iteration
                # from polygons up or down
                x = [row["base_point_x"], row["px"]],
                y = [row["base_point_y"], row["py"]],
                for x1, y1 in zip(x, y):
                    self.msp.add_line(
                        start=(x1[0], y1[0]),
                        end=(x1[1], y1[1]),
                        dxfattribs={"color": PLOTLY_COLORS.get(row["color"], 1)})
                self.__add_equipment_marker(row, en, data_for_plotting)

    def export_to_mpl(self):
        # Safe loading procedure (requires ezdxf v0.14):
        try:
            doc, auditor = recover.readfile(self.doc_name)
        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)

        # The auditor.errors attribute stores severe errors,
        # which may raise exceptions when rendering.
        if not auditor.has_errors:
            plt.figure(facecolor='white')
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(doc)
            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
            fig.savefig('scheme.svg')
