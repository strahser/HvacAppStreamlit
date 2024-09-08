import pandas as pd
import streamlit
from ezdxf.enums import TextEntityAlignment

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Dxf.DxfBlockCreator import DxfBlockCreator, BlockNames, BlockLayers
from PrincipalSchems.Dxf.DxfConstants import PLOTLY_COLORS, TEXT_PROPERTY
from PrincipalSchems.Dxf.DxfDocument import DxfDocument


class DxfDrawEquipmentData:
	def __init__(self, data_for_plotting: DataForPlotting, creator: DxfBlockCreator):
		self.doc = DxfDocument.doc
		self.msp = DxfDocument.msp
		self.data_for_plotting = data_for_plotting
		self.creator = creator
		self.level_column = data_for_plotting.polygon_points_merge_control.layout_view_context_data.level_column
		self.location_point_list = data_for_plotting.location_point_list
		self.dynamic_widgets_data = data_for_plotting.dynamic_widgets_view_context_data
		self.equipment_point_list = pd.concat(self.location_point_list)\
			.groupby(["system_name","base_point_x","base_point_y","px","py","color"])\
			.size().reset_index(name='counts')		#не используется

	def __get_equipment_text(self, row, en):
		level_text = row[self.data_for_plotting.polygon_points_merge_control.layout_view_context_data.level_column]
		system_flow = self.data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]
		text = f"{level_text}система:{row['system_name']}расход:{system_flow}"
		return text

	def __add_equipment_marker(self, marker_coordinates:[tuple[float,float]],system_text,block_symbol):
		"""row in location_point_list """
		self.msp.add_blockref(name=getattr(BlockNames, block_symbol).value, insert=marker_coordinates,
		                      dxfattribs={'layer': getattr(BlockLayers,block_symbol).value,
		                                  'xscale': 2,
		                                  'yscale': 2},
		                      )
		self.msp.add_text(system_text, dxfattribs=TEXT_PROPERTY) \
			.set_placement((marker_coordinates[0],
		                    marker_coordinates[1] + 20),
		                   align=TextEntityAlignment.LEFT)

	def plot_horizontal_line_to_equipment(self):
		"""Доводим горизонтальюную линюю смещения до точки расположения оборудования"""
		for en, df in enumerate(self.location_point_list):  # levels iteration
			for idx_, row in df.iterrows():  # df row iteration
				equipment_symbol = self.data_for_plotting.dynamic_widgets_view_context_data.equipment_symbol_list[en]
				marker_coordinates = (row["base_point_x"], row["base_point_y"])
				system_flow = self.data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]
				text = self.__get_equipment_text(row,en)
				# from polygons up or down
				x = [row["base_point_x"], row["px"]],
				y = [row["base_point_y"], row["py"]],
				if row["system_name"] not in self.doc.layers:
					self.doc.layers.add(row["system_name"], color=PLOTLY_COLORS.get(row["color"], 1))
				for x1, y1 in zip(x, y):
					self.msp.add_line(
						start=(x1[0], y1[0]),
						end=(x1[1], y1[1]),
						dxfattribs={'layer': row["system_name"]
						            }
					)

				self.__add_equipment_marker(marker_coordinates,text,equipment_symbol)
