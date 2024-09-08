"""
pip install pipwin

pipwin install cairocffi
"""
from PrincipalSchems.Dxf.DxfBlockCreator import BlockNames


class StaticTabsView:
	"""add tabs names"""

	tabs = [
		"main input",
		"space and level dimensions",
		"equipment config",
		"system detail config",
		"plot config"
	]


class MainSchemeConfig:
	"""data for system direction,system color
    """
	vertical_direction_list = ["up", "down"]
	horizontal_direction_list = ["left", "right"]
	colors = [
		"orange", "indigo", "lightpink", "darkblue", "firebrick", "orchid",
		"yellowgreen", "goldenrod", "blue", "brown", "red", "coral",
		"darkmagenta", "green", "cyan", "deeppink"
	]


class EquipmentSymbol:
	symbols = {
		BlockNames.SUPPLY_AIR.name: "Приточная установка ",
		BlockNames.EXHAUST_AIR.name: "Крышный вентилятор",
	}
	names = []
