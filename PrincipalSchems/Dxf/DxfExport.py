import datetime

import ezdxf
import pandas as pd
import streamlit
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Dxf.DxfBlockCreator import DxfBlockCreator
from PrincipalSchems.Dxf.DxfConstants import TEXT_PROPERTY, PLOTLY_COLORS
from PrincipalSchems.Dxf.DxfDocument import DxfDocument
from PrincipalSchems.Dxf.DxfDrawAllSchemLines import DxfDrawAllSchemLines
from PrincipalSchems.Dxf.DxfDrawEquipmentData import DxfDrawEquipmentData
from PrincipalSchems.Dxf.DxfDrawLevelData import DxfDrawLevelData
from PrincipalSchems.Dxf.DxfDrawPolygons import DxfDrawPolygons
from PrincipalSchems.Dxf.DxfDrawSystemLine import plot_vertical_side_plot_lines_to_system


class DxfExport:
    # Создаем новый чертеж
    doc = DxfDocument.doc
    msp = DxfDocument.msp
    doc.layers.add('Polygons', color=colors.GRAY)
    time_suffix = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    doc_name = f"schem.dxf"
    text_y_offset = 5

    def __init__(self, data_for_plotting: list[DataForPlotting]):
        self.clean_dxf()
        self.data_for_plotting = data_for_plotting
        self.polygon_points_merge_control_0 = data_for_plotting[0].polygon_points_merge_control
        self.color_view_checkbox = self.polygon_points_merge_control_0.layout_view_context_data.color_view_checkbox
        self.color_filter_name = self.polygon_points_merge_control_0.layout_view_context_data.space_data_view.color_filter_name
        self.creator = DxfBlockCreator(self.doc)
        self.text_worker_df = self.polygon_points_merge_control_0.text_worker.df
        self.creator = DxfBlockCreator(self.doc)

    def get_color_legend_data(self) -> pd.DataFrame:
        return self.text_worker_df.groupby([self.color_filter_name, 'color']) \
            .count().reset_index().filter([self.color_filter_name, 'color'])

    def clean_dxf(self):

        types_to_delete = {"LINE", "LWPOLYLINE", "POLYLINE", "TEXT", "MTEXT"}

        # Удаление объектов указанных типов
        for entity in self.msp.query("*"):
            if entity.dxftype() in types_to_delete:
                self.msp.delete_entity(entity)
            # Удаление блоков из чертежа
        for block_name in self.doc.blocks:
            # Пропускаем блок MODEL_SPACE
            if block_name.name == 'MODEL_SPACE':
                continue
            block = self.doc.blocks[block_name.name]

    def add_color_legend_title(self, start_x, start_y):
        self.msp.add_text(f"Категория Легенды {self.color_filter_name}", dxfattribs=TEXT_PROPERTY) \
            .set_placement((start_x, start_y),
                           align=TextEntityAlignment.LEFT)

    def create_color_legend(self, start_legend_coordinates: float) -> float:
        start_x = 1000
        start_y = 1000 + start_legend_coordinates
        increment = 0
        line_length = 20
        if self.color_view_checkbox:
            for idx, row in self.get_color_legend_data().iterrows():
                if PLOTLY_COLORS.get(row["color"]):
                    self.msp.add_line(start=(start_x, start_y + increment),
                                      end=(start_x + line_length, start_y + increment),
                                      dxfattribs={'color': PLOTLY_COLORS.get(row["color"])}
                                      )
                    self.msp.add_text(row[self.color_filter_name], dxfattribs=TEXT_PROPERTY) \
                        .set_placement((start_x + line_length + 5, start_y + increment),
                                       align=TextEntityAlignment.LEFT)
                increment += 20
            self.add_color_legend_title(start_x, start_y + increment)
            return increment

    def export_to_dxf_data(self):
        self.creator.create_blocks_if_not_exists()
        streamlit.success("DXF Создано")
        polygons = DxfDrawPolygons(self.text_worker_df)
        polygons.plot_space_polygons_and_text(color_filter_name=self.color_filter_name,
                                              show_color=self.color_view_checkbox)
        level_data = DxfDrawLevelData()
        level_data.add_level_text(self.data_for_plotting[0])
        start_legend_coordinates = 0

        for plotting_data in self.data_for_plotting:
            equipment_data = DxfDrawEquipmentData(plotting_data, self.creator)
            equipment_data.plot_horizontal_line_to_equipment()
            all_schemes_lines = DxfDrawAllSchemLines(plotting_data)
            all_schemes_lines.plot_start_end_system_lines()
            all_schemes_lines.add_level_flow_()
            color_df = plotting_data.polygon_points_merge_control.add_color_df  # system and color
            plot_vertical_side_plot_lines_to_system(self.msp, color_df)
            offset_value = all_schemes_lines.draw_legend(start_legend_coordinates)
            start_legend_coordinates += offset_value
        self.create_color_legend(start_legend_coordinates)

        self.doc.saveas(self.doc_name)
