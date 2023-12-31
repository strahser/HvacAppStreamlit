import json
from Session.CreateViewFromStatementModel import CreateViewFromStatementModel
from StaticData.AppHelp import AppHelp
import streamlit as st


class UploadSessionSetting:
	def __init__(self, uploaded_session_file: st.file_uploader):

		self.uploaded_session_file = uploaded_session_file
		self.uploaded_settings = None

	def show_session_view(self):
		st.subheader("Upload settings")
		self._create_upload_view()
		self._create_upload_db_from_setting_button()

	def _create_upload_settings(self):
		"""Set session state values to what specified in the json_settings."""
		if self.uploaded_settings:
			for k in self.uploaded_settings.keys():
				try:
					st.session_state[k] = self.uploaded_settings[k]
				except Exception as e:
					st.warning(e)
		else:
			st.warning("**WARNING**: Select the Settings File to be uploaded")

	def _create_upload_view(self):
		# 2. Select Settings to be uploaded
		self._apply_upload_settings_view()
		if self.uploaded_session_file:
			try:
				self.uploaded_settings = json.load(self.uploaded_session_file)
			except:
				st.warning("**WARNING**: Select the Settings File to be uploaded")
				self.uploaded_settings = None

	def _apply_upload_settings_view(self):
		apply_setting_button = st.button(label="Apply Settings",
		                                 on_click=self._create_upload_settings,
		                                 # args=(self.uploaded_settings,),
		                                 key="Apply Settings button",
		                                 help=AppHelp.button_apply_settings)

	def _create_upload_db_from_setting_button(self):
		self.load_statement_model_button = st.button("Load Statement Model",
		                                             key=f"load statement model button",
		                                             help=AppHelp.session_view_create
		                                             )
		if self.load_statement_model_button:
			self.create_statement_model = CreateViewFromStatementModel()
			self.create_statement_model.parsing_session_statement()



