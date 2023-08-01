import pandas as pd
import streamlit as st
from collections import namedtuple
from collections import defaultdict
from itertools import cycle
"""
pip install pipwin

pipwin install cairocffi
"""
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
		"square-x": "roof exaust",
		"circle-x": "canal vent",
		"star-diamond": "AHU",
		"triangle-up": "",
		"triangle-down": "",
		"triangle-left": "",
		"triangle-right": "",
		"asterisk-open": "axis vent",
		"pentagon": "AHU",
		"hash-open": "",
	}
	names = []
