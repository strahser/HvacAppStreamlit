import streamlit
from ezdxf.enums import TextEntityAlignment
from enum import Enum, auto


class BlockNames(Enum):
	SUPPLY_AIR = 'supply_air_unit'
	EXHAUST_AIR = 'exhaust_roof_air_unit'

	@classmethod
	def choices(cls):
		"""Возвращает список выборов для BlockType в виде пар (значение, имя)."""
		return [member.name for member in cls]


class BlockLayers(Enum):
	SUPPLY_AIR = 'supply_air_block_layer'
	EXHAUST_AIR = 'exhaust_air_block_layer'


class DxfBlockCreator:

	def __init__(self, doc):
		self.doc = doc
		self.block_factory = {BlockNames.SUPPLY_AIR.value: self.create_supply_unit_block,
		                 BlockNames.EXHAUST_AIR.value: self.create_roof_fan_block,
		                 }
		self.add_layers_and_blocks_if_not_exists()

	def add_layers_and_blocks_if_not_exists(self):

		for data in BlockNames.choices():
			block_name = getattr(BlockNames, data).value
			block_layer = getattr(BlockLayers, data).value
			if block_layer not in self.doc.layers:
				self.doc.layers.add(block_layer, color=2)
			if block_name not in self.doc.blocks:
				self.block_factory[block_name]()

	def create_supply_unit_block(self, width=10, height=5):
		"""
        Создает блок условного обозначения приточной установки в DXF-чертеже.

        Args:
            width: Ширина блока.
            height: Высота блока.
        """

		block = self.doc.blocks.new(name=BlockNames.SUPPLY_AIR.value)
		block_air_attr = {'layer': BlockLayers.SUPPLY_AIR.value}

		section_width = width / 3

		# Рисуем прямоугольник
		block.add_lwpolyline(points=[
			(0, 0),
			(width, 0),
			(width, height),
			(0, height),
			(0, 0)
		], dxfattribs=block_air_attr)

		# Разделяем прямоугольник на секции
		for i in range(1, 3):
			block.add_line(start=(i * section_width, 0), end=(i * section_width, height),
			               dxfattribs=block_air_attr)

		# Рисуем вентилятор
		block.add_circle(center=(section_width / 2, height / 2), radius=height / 4,
		                 dxfattribs=block_air_attr)
		block.add_line(start=(section_width / 4, height / 2), end=(3 * section_width / 4, height / 2),
		               dxfattribs=block_air_attr)

		# Рисуем теплообменник
		block.add_text(text="+",
		               dxfattribs=block_air_attr).set_placement(
			(section_width * 1.5, height / 2), align=TextEntityAlignment.CENTER)
		block.add_text(text="-",
		               dxfattribs=block_air_attr).set_placement(
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
		], dxfattribs=block_air_attr)

	def create_roof_fan_block(self, width=5, height=8, visor_height=2):
		"""
        Создает блок условного обозначения крышного вентилятора в DXF-чертеже.

        Args:
            block_name: Имя создаваемого блока.
            width: Ширина блока.
            height: Высота блока.
            visor_height: Высота козырька.
        """
		block = self.doc.blocks.new(name=BlockNames.EXHAUST_AIR.value)
		block_attr = {'layer': BlockLayers.EXHAUST_AIR.value}
		# Рисуем прямоугольник
		block.add_lwpolyline(points=[
			(0, 0),
			(width, 0),
			(width, height),
			(0, height),
			(0, 0)
		], dxfattribs=block_attr)

		# Рисуем козырек
		block.add_lwpolyline(points=[
			(width / 2, height),
			(width, height - visor_height),  # Изменена вторая точка
			(0, height - visor_height),  # Изменена третья точка
			(width / 2, height)
		], dxfattribs={'layer': 'Вентиляторы'})

		# Рисуем вентилятор (цифра 8 из окружностей)
		center_x = width / 2
		radius = width / 4
		block.add_circle(center=(center_x, height / 2), radius=radius, dxfattribs={'layer': 'Вентиляторы'})
		block.add_circle(center=(center_x, height / 2 + radius), radius=radius, dxfattribs={'layer': 'Вентиляторы'})

	def create_blocks_if_not_exists(self):
		if not BlockNames.SUPPLY_AIR.value in self.doc.blocks:
			self.create_supply_unit_block()
		if not BlockNames.EXHAUST_AIR.value in self.doc.blocks:
			self.create_roof_fan_block()

	@staticmethod
	def __add_attrib(blockref, attr_value: str, coordinates: [tuple[float, float]]) -> None:
		blockref.add_attrib(tag='system_name', text=attr_value, dxfattribs={'invisible': False, 'height': 2, }) \
			.set_placement((coordinates[0], coordinates[1] + 12))
