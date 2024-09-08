import pandas as pd
from PrincipalSchems.Dxf.DxfConstants import TEXT_PROPERTY, PLOTLY_COLORS
from ezdxf import colors

from PrincipalSchems.Dxf.DxfDocument import DxfDocument


class DxfDrawPolygons:

	def __init__(self, text_worker_df: pd.DataFrame):
		"""text_worker_df polygon_points_merge_control.text_worker.df
			text_worker_df  Таблица с текстом полигона  px,py,pcx,pcy,color
		"""
		self.doc = DxfDocument.doc
		self.msp = DxfDocument.msp
		self.text_worker_df = text_worker_df

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
