from ezdxf.enums import TextEntityAlignment

from PrincipalSchems.Dxf.DxfConstants import TEXT_PROPERTY
from PrincipalSchems.Dxf.DxfDocument import DxfDocument
import streamlit as st


class DxfDrawLevelData:

	def __init__(self):
		self.msp = DxfDocument.msp

	def add_level_text(self, data_for_plotting):
		"""Размещаем Текст Название уровня на чертеже"""
		level_property = data_for_plotting.polygon_points_merge_control.get_level_property()
		for prop in level_property:
			self.msp.add_text(
				prop.level_name,
				height=6,
				dxfattribs=TEXT_PROPERTY).set_placement(
				(prop.level_coord_x, prop.level_coord_y),
				align=TextEntityAlignment.CENTER
			)
