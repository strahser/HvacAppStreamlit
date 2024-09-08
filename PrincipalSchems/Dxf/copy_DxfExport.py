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


class DxfExport:
	# Создаем новый чертеж
	doc = DxfDocument.doc
	msp = DxfDocument.msp
	doc.layers.add('Polygons', color=colors.GRAY)
	doc_name = "rectangles.dxf"
	text_y_offset = 5

	def __init__(self, data_for_plotting: list[DataForPlotting]):
		self.data_for_plotting = data_for_plotting
		# polygon_points_merge_control_0 Для  полигонов, надписи уровня
		self.polygon_points_merge_control_0 = data_for_plotting[0].polygon_points_merge_control
		self.creator = DxfBlockCreator(self.doc)

	def export_to_dxf_data(self):
		self.creator.create_blocks_if_not_exists()
		self.plot_space_polygons_and_text()
		self.__plot_horizontal_line_to_equipment()
		self.add_level_text()
		all_data = []
		start_point = [2000, 500]
		increment = 20
		for data in self.data_for_plotting:
			data_system = self.plot_start_end_system_lines(data)
			all_data.extend(data_system)

		all_data = sorted(all_data)
		for data in all_data:
			self.msp.add_line(
				start=(start_point[0], start_point[1]),
				end=(start_point[0] + 100, start_point[1]),
				dxfattribs={'layer': data[0]})
			self.msp.add_text(
				data[0],
				dxfattribs=TEXT_PROPERTY).set_placement((start_point[0] + 120, start_point[1]),
			                                            align=TextEntityAlignment.LEFT)
			start_point[1] -= increment
		self.save()

	def add_level_text(self):
		"""Размещаем Текст Название уровня на чертеже"""
		level_property = self.polygon_points_merge_control_0.get_level_property()
		for prop in level_property:
			self.msp.add_text(
				prop.level_name,
				dxfattribs=TEXT_PROPERTY).set_placement(
				(prop.level_coord_x, prop.level_coord_y),
				align=TextEntityAlignment.CENTER
			)

	@property
	def text_worker_df(self):
		"""text_worker_df  Таблица с текстом полигона  px,py,pcx,pcy,color"""
		return self.polygon_points_merge_control_0.text_worker.df

	def save(self):
		self.doc.saveas(self.doc_name)


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

	def plot_start_end_system_lines(self, data_for_plotting: DataForPlotting) -> set[tuple[str, str]]:
		def __add_system_flow_and_arrow_to_space() -> None:
			_text = f" {point.system_name}\n L={str(point.system_flow)}"
			mtext = self.msp.add_mtext(_text, dxfattribs=TEXT_PROPERTY)
			mtext.dxf.insert = (point.x_start_points + 5, point.y_start_points + 10)
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

			for idx, row in level_system_point_group_df.iterrows():
				if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
					level_points = (point.offset_point_x, point.offset_point_y)
					level_text = f"{point.level_value} {point.system_name}L = {round(row['system_flow'])}"
					add_system_name_text()

		def __add_vertical_line_from_polygons():
			"""из каждого помещения добавляет линию"""

			if point.system_name not in self.doc.layers:
				self.doc.layers.add(point.system_name, color=PLOTLY_COLORS.get(point.color, 1))
			self.msp.add_line(
				start=(point.x_start_points, point.y_start_points),
				end=(point.x_end_points, point.y_end_points),
				dxfattribs={'layer': point.system_name})

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
			if point.system_name not in self.doc.layers:
				self.doc.layers.add(point.system_name, color=PLOTLY_COLORS.get(point.color, 1))
			self.msp.add_line(
				start=offset_start,
				end=offset_end,
				dxfattribs={'layer': point.system_name})

		def __plot_vertical_side_plot_lines_to_system():
			# between levels
			st.write("data_for_plotting.polygon_points_merge_control.add_color_df")
			st.write(data_for_plotting.polygon_points_merge_control.add_color_df)
			for idx_, row in data_for_plotting.polygon_points_merge_control.add_color_df.iterrows():
				self.msp.add_line(
					start=(row["Max_x"], row["Max_y"]),
					end=(row["Min_x"], row["Min_y"]),
					dxfattribs={'layer': row["system_name"]})

		_system_points = data_for_plotting.polygon_points_merge_control.system_property_points
		# группируем и получаем  по системам в каждой точке offset_point   "system_flow"
		level_system_point_group_df = pd.DataFrame([prop.__dict__ for prop in _system_points]) \
			.groupby(['system_name', 'offset_point_x', 'offset_point_y'])["system_flow"] \
			.sum().reset_index()
		st.write("level_system_point_group_df")
		st.write(level_system_point_group_df)
		unique_points = set()
		st.write("system_points_list")
		st.dataframe([val.__dict__ for val in _system_points])
		for point in _system_points:
			__add_system_flow_and_arrow_to_space()  # add flow
			__add_level_flow_()  # add offset sum flow
			__add_vertical_line_from_polygons()  # from polygons up or down
			__add_horizontal_system_lines_to_level_point()
			__plot_vertical_side_plot_lines_to_system()
			unique_points.add((point.system_name, point.color))
		return unique_points

	def __add_equipment_marker(self, row, en, data_for_plotting: DataForPlotting):
		def __get_equipment_text():
			level_text = row[data_for_plotting.polygon_points_merge_control.layout_view_context_data.level_column]
			system_flow = data_for_plotting.dynamic_widgets_view_context_data.flow_list_value[en]
			text = f"{row['system_name']} {system_flow}"
			return text

		# equipment_symbol = self.data_for_plotting[0].dynamic_widgets_view_context_data.equipment_symbol_list[en]
		text_coordinates = (row["base_point_x"], row["base_point_y"])
		self.msp.add_blockref(name=self.creator.exhaust_air_block_name, insert=text_coordinates,
		                      dxfattribs={'layer': self.creator.exhaust_air_block_layer,
		                                  'xscale': 2,
		                                  'yscale': 2},
		                      )
		self.msp.add_text(__get_equipment_text(), dxfattribs=TEXT_PROPERTY).set_placement((text_coordinates[0],
		                                                                                   text_coordinates[1] + 20),
		                                                                                  align=TextEntityAlignment.LEFT)

	def __plot_horizontal_line_to_equipment(self):
		"""Доводим горизонтальюную линюю смещения до точки расположения оборудования"""
		st.write("location_point_list")
		st.write(pd.concat(self.data_for_plotting[0].location_point_list))
		for en, df in enumerate(self.data_for_plotting[0].location_point_list):  # levels iteration
			for idx_, row in df.iterrows():  # df row iteration
				# from polygons up or down
				x = [row["base_point_x"], row["px"]],
				y = [row["base_point_y"], row["py"]],
				if row["system_name"] not in self.doc.layers:
					self.doc.layers.add(row["system_name"], color=PLOTLY_COLORS.get(row["color"], 1))
				for x1, y1 in zip(x, y):
					self.msp.add_line(
						start=(x1[0], y1[0]),
						end=(x1[1], y1[1]),
						dxfattribs={'layer': row["system_name"]}
					)
				self.__add_equipment_marker(row, en, self.data_for_plotting[0])

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
