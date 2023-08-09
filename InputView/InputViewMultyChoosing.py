from Upload.UploadLayout import UploadLayout
import streamlit as st
from InputView.InputViewControl import InputViewControl
import pandas as pd
from InputView.InputViewModel.PreselectValueModel import PreselectValueModel


class InputViewMultyChoosing:
	def __init__(self, upload_layout: UploadLayout, key):
		"""select data for terminals calculation"""
		self.upload_layout = upload_layout
		self.table_dict = self.upload_layout.table_dict
		self.key = key

	def check_input_data_loaded(self,
	                            excel_sheet_names: list[str],
	                            class_instance,
	                            ) -> bool:
		"""check if all excel/pandas tables loaded?"""
		st.subheader("select sheet data")
		with st.expander("select sheet data"):
			confirm_checkbox = st.checkbox("Confirm Sheet Data", key=f"{self.key} confirm_checkbox")
			for name in excel_sheet_names:
				st.subheader(f"Select {name.replace('_', ' ')} file")
				input_view_control = InputViewControl(self.upload_layout, key=f"{str(self.key)} {name}")
				excel_book = self._select_excel_index(name)
				if excel_book and isinstance(excel_book,list):
					try:
						check_input_df = [
							pd.read_sql(f"select * from {sheet}", con=input_view_control.connector) for sheet in excel_book
						]
						setattr(class_instance, name, check_input_df)
					except Exception as e:
						st.warning(e)

				else:
					check_input_df = input_view_control.create_input_view(index_book=self.index_book,
					                                                      index_sheet=self.index_sheet)
					setattr(class_instance, name, check_input_df)
			if  confirm_checkbox:
				return True
			else:
				st.warning("Check is all selected excel sheets  exist?")

	def _select_excel_index(self, search_sheet: str):

		preselect_ = PreselectValueModel(self.upload_layout.table_dict)
		preselect_.preselect_data(search_sheet)
		self.all_sheets_checkbox = st.checkbox("all sheets?", value=preselect_.all_sheets,
		                                       key=f"{self.key} all_sheets_checkbox_ {search_sheet}")
		self.index_book = preselect_.index_book
		self.index_sheet = preselect_.index_sheet
		if self.all_sheets_checkbox:
			return self.table_dict[search_sheet]
		else:return search_sheet



