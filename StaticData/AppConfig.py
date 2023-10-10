from dataclasses import dataclass
from Session.StatementConfig import StatementConstants
import streamlit as st
from enum import Enum


@dataclass()
class MenuChapters:
	dash_board: str = "Dash Board"
	ifc_dash_board: str = "IFC"
	analytics: str = "Analytics"
	polygons: str = "Zones"
	scheme: str = "Scheme"
	terminals: str = "Terminals"
	Networks:str = "Networks"
	ahu: str = "AHU"
	download: str = "Downloads"
	menu_list = ["dash_board",
		             "ifc_dash_board",
		             "polygons",
		             "scheme",
		             "terminals",
		             "Networks",
		             "ahu",
		             "download"]

	@staticmethod
	def get_buttons():
		return [getattr(MenuChapters, name) for name in MenuChapters.menu_list]


@dataclass()
class MenuIcons:
	dash_board: str = "bi bi-table"
	ifc_dash_board: str = "bi bi-cloud-upload"
	analytics: str = "bi bi-table"
	polygons: str = "bi bi-building add"
	scheme: str = "bi bi-diagram-3-fill"
	Networks: str = "bi bi-diagram-3-fill"
	ahu: str = "bi bi-puzzle fill"
	terminals: str = "bi bi-dice-6-fill"
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
	excel_sheet_names_AHU = ["revit_export", "medium_property"]
