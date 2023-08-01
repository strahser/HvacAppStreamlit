from dataclasses import dataclass
from Session.StatementConfig import StatementConstants
import streamlit as st
from enum import Enum


class Language:
	def __init__(self):
		self.language = st.sidebar.selectbox("Select Language", ['ru', 'en'])


def _(s, language="en"):
	ruStrings = {"Choose Option Style": 'Выберите стиль меню',
	             "Hydralit Style": "Гидралит Стиль",
	             "Button Style": "Обычный Стиль",
	             "Input Data": "Исходные Данные",
	             "Zones": "Зонирование"
	             }

	if language == 'en':
		return s
	if language == 'ru':
		return ruStrings.get(s, s)


@dataclass()
class MenuChapters:
	dash_board: str = _("Dash Board")
	ifc_dash_board:str =_("IFC")
	analytics: str = _("Analytics")
	polygons: str = _("Zones")
	scheme: str = _("Scheme")
	terminals: str = _("Terminals")
	ahu: str = _("AHU")
	download: str = _("Downloads")

	@staticmethod
	def get_buttons():
		return [getattr(MenuChapters, name) for name in MenuChapters.__annotations__.keys()]


@dataclass()
class MenuIcons:
	dash_board: str = "bi bi-cloud-upload"
	ifc_dash_board: str = "bi bi-cloud-upload"
	polygons: str = "bi bi-building add"
	scheme: str = "bi bi-diagram-3-fill"
	ahu: str = "bi bi-puzzle fill"
	terminals: str = "bi bi-dice-6-fill"
	analytics: str = "bi bi-table"
	download: str = "bi bi-cloud-download-fill"

	@staticmethod
	def get_icons():
		return [getattr(MenuIcons, name) for name in MenuIcons.__annotations__.keys()]


class StaticVariable(Enum):
	load_excel = "load Excel"
	load_db = "load DB"


class ExcelSheetsLoads:
	"""to find correct sheet (create view )"""
	excel_sheet_names_Terminal = ['revit_export', 'EquipmentBase', 'devices', 'device_type', "config",
	                              'device_orientation']
	excel_sheet_names_AHU = ["revit_export", "input_excel_AHU", "medium_property"]
