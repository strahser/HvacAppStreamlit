import streamlit as st

from StaticData.AppConfig import StaticVariable

from st_mui_dialog import st_mui_dialog

from Session.UpdateDbSession import UpdateDbSession


class UploadView:

	def get_upload_layout(self):
		st.subheader("Choose Excel or DB load")
		self.select_db_or_excel = st.radio(label="Choose Excel or DB load",
		                                   options=[StaticVariable.load_excel.value, StaticVariable.load_db.value],
		                                   horizontal=True,
		                                   label_visibility="collapsed")
		if self.select_db_or_excel == StaticVariable.load_excel.value:
			st.subheader("Choose  Excel Files")
			self.input_excel_sheet_uploader = st.file_uploader("Choose  Excel Files",
			                                                   accept_multiple_files=True,
			                                                   type=["xlsx", "xlsm"])
		else:
			st.subheader('Choose DB for update')
			self.upload_db = st.file_uploader("Choose DB for update", type="sql")
		st.subheader('Choose a JSON Polygons file for Plots')
		self.file_json_upload = st.file_uploader("Choose a JSON Polygons file", type="json")
		self.update_db_button = st.button("Update Data?", on_click=UpdateDbSession.Update_sql_sessionData)
		UpdateDbSession.create_modal_window(key="DB All Tables Show")

	def __create_upload_modal(self):
		key = "Manual Modal Window"
		answer = st_mui_dialog(
			title="All DB Tables",
			content="\n,".join(self.all_db_tables),
			styling_open_button="""{"backgroundColor" :"lightgreen"}""",
			button_txt="Show Loaded Data Bases",
		)
