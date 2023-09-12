from dataclasses import dataclass

import pandas as pd
import streamlit as st
import inspect
import os
import sys

from InputView.InputViewModel.InputViewLoadDFfromStatment import create_input_choosing_data_form
from SQL.SqlModel.SqlConnector import SqlConnector
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import ExcelSheetsLoads

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from AhuLayout.Control.AHUControl import AHUControl
from InputView.InputViewMultyChoosing import InputViewMultyChoosing
from Upload.UploadLayout import UploadLayout


@dataclass
class AhuTable:
	pass


def MainAHU(upload_layout: UploadLayout, key):
	col = st.columns(2)
	with col[0].expander("__AHU Calculation file__"):
		input_excel_AHU = st.file_uploader("Choose  AHU Excel Book", type=["xlsx", 'xlsm'])

	@st.cache_data
	def _get_input_excel_AHU_files_loads():
		input_excel_AHU_files_loads = pd.read_excel(input_excel_AHU, sheet_name=None, skiprows=14, nrows=10)
		return input_excel_AHU_files_loads

	multy_load = InputViewMultyChoosing(upload_layout, key=key)
	multy_load.check_input_data_loaded(ExcelSheetsLoads.excel_sheet_names_AHU, StatementConstants.ahu_names_dict)
	check_input_data = len(st.session_state[StatementConstants.ahu_names_dict].keys()) == len(
		ExcelSheetsLoads.excel_sheet_names_AHU)
	ahu_table = AhuTable
	for key, value in st.session_state[StatementConstants.ahu_names_dict].items():
		connector = SqlConnector.conn_sql
		df = pd.read_sql(f"select * from {value}", con=connector)
		setattr(ahu_table, value, df)
	if check_input_data and input_excel_AHU:
		input_excel_AHU_files_loads = _get_input_excel_AHU_files_loads()
		ahu_view = AHUControl(
			ahu_table.revit_export,
			ahu_table.medium_property,
			input_excel_AHU_files_loads,
			key=f"{key}"
		)
		ahu_view.create_ahu_data_tab()
		if ahu_view.system_columns_name:
			ahu_view.create_pivot_tab()
			ahu_view.create_download_tab()
	else:
		st.write("Please Choose  AHU Excel Book")
