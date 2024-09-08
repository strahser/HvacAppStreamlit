import datetime
import sys
from io import BytesIO, StringIO
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
		self.data_for_plotting = data_for_plotting
		self.polygon_points_merge_control_0 = data_for_plotting[0].polygon_points_merge_control
		self.creator = DxfBlockCreator(self.doc)
		self.text_worker_df = self.polygon_points_merge_control_0.text_worker.df
		self.creator = DxfBlockCreator(self.doc)

	def export_to_dxf_data(self):
		self.creator.create_blocks_if_not_exists()
		polygons = DxfDrawPolygons(self.text_worker_df)
		polygons.plot_space_polygons_and_text()
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
		self.doc.saveas(self.doc_name)
