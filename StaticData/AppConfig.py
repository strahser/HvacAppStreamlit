from dataclasses import dataclass
from Session.StatementConfig import StatementConstants
import streamlit as st
from enum import Enum


@dataclass()
class MenuChapters:
	Networks:str = "Networks"
	dash_board: str = "Dash Board"
	ifc_dash_board: str = "IFC"
	analytics: str = "Analytics"
	polygons: str = "Zones"
	scheme: str = "Scheme"
	terminals: str = "Terminals"
	ahu: str = "AHU"
	download: str = "Downloads"

	@staticmethod
	def get_buttons():
		return [getattr(MenuChapters, name) for name in MenuChapters.__annotations__.keys()]


@dataclass()
class MenuIcons:
	Networks: str = "bi bi-diagram-3-fill"
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
	excel_sheet_names_AHU = ["revit_export", "medium_property"]
