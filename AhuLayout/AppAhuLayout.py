import pandas as pd
import streamlit as st
import inspect
import os
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from AhuLayout.Control.AHUControl import AHUControl
from InputView.InputViewMultyChoosing import InputViewMultyChoosing
from Upload.UploadLayout import UploadLayout


def MainAHU(upload_layout: UploadLayout, key):
	excel_sheet_names_AHU = ["revit_export", "medium_property"]
	with st.expander("__AHU Calculation file__"):
		input_excel_AHU = st.file_uploader("Choose  AHU Excel Book", type=["xlsx", 'xlsm'])

	@st.cache_data
	def _get_input_excel_AHU_files_loads():
		input_excel_AHU_files_loads = pd.read_excel(input_excel_AHU, sheet_name=None, skiprows=14, nrows=10)
		return input_excel_AHU_files_loads
	if input_excel_AHU:
		input_excel_AHU_files_loads = _get_input_excel_AHU_files_loads()
		multy_load = InputViewMultyChoosing(upload_layout, key=key)
		confirm_load = multy_load.create_input_choosing_data_form(excel_sheet_names_AHU, multy_load)
		if confirm_load:
			ahu_view = AHUControl(
				multy_load.revit_export,
				multy_load.medium_property,
				input_excel_AHU_files_loads,
				key=f"{key}"
			)
			ahu_view.create_ahu_data_tab()
			if ahu_view.system_columns_name:
				ahu_view.create_pivot_tab()
				ahu_view.create_download_tab()
	else:
		st.write("Please Choose  AHU Excel Book")
