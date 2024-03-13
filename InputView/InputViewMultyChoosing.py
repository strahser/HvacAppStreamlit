from Upload.UploadLayout import UploadLayout
import streamlit as st
from InputView.InputViewControl import InputViewControl


class InputViewMultyChoosing:
	def __init__(self, upload_layout: UploadLayout, key):
		"""
		select data for multy choosing table from session dict
		"""
		self.show_input_data = None
		self.upload_layout = upload_layout
		self.table_dict = self.upload_layout.table_dict
		self.key = key

	def check_input_data_loaded(self, excel_sheet_names: list[str], statement_constant_name: str) -> None:
		"""
		excel_sheet_names:list[str] - names of requirement excel/sql tables for product
		statement_constant_name:str dict key from  st.session_state[statement_constant_name] to save default value
		check if all excel/pandas tables loaded? add to session_state dictionary of list
		"""
		self.show_input_data = st.checkbox("Add Data For Calculations", key=f"{self.key} show_input_data")
		placeholder = st.empty()
		if self.show_input_data:
			with placeholder.container():
				st.subheader("select sheet data")
				with st.expander("+"):
					temp_dict = {}
					for name in excel_sheet_names:
						st.write(f"Select {name.replace('_', ' ')} file")
						with st.expander("+"):
							input_view_control = InputViewControl(self.upload_layout, key=f"{str(self.key)} {name}")
							all_sheets_check_box = st.checkbox("All sheets", key=f"all sheets name {name}")
							input_view_control.create_input_view()
							if all_sheets_check_box:
								sheet_name = input_view_control.input_view.all_selected_sheet
								temp_dict[name] = sheet_name
							else:
								sheet_name = input_view_control.sheet_name
								temp_dict[name] = sheet_name
					submit_button = st.button("Submit", key="submit terminal button")
					if submit_button and len(temp_dict.keys()) == len(excel_sheet_names):
						st.session_state[statement_constant_name] = temp_dict
						st.success("You just have loaded")
						st.success(st.session_state[statement_constant_name])
