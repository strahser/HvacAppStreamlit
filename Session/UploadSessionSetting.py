import json

from Session.CreateViewFromStatementModel import CreateViewFromStatementModel
from Session.StatementConfig import StatementConstants, SettingConfig
from StaticData.AppHelp import AppHelp
from Session.AutoloadSession import AutoloadSession
import streamlit as st

from library_hvac_app.list_custom_functions import flatten


class UploadSessionSetting:
	def __init__(self, uploaded_session_file: st.file_uploader):

		self.uploaded_session_file = uploaded_session_file
		self.uploaded_settings = None

	def show_session_view(self):
		col1, col2 = st.columns([6, 5])
		with col1:
			self._create_upload_view()
			self._create_upload_db_from_setting_button()
		with col2:
			self._create_download_settings()

	def _create_excluding_session_dictionary(self):
		excluding_list = SettingConfig.excluding_list

		all_keys = st.session_state.keys()
		correct_keys = []
		for excl_val in excluding_list:
			temp_list =[]
			for k in all_keys:
				if excl_val  in k:
					temp_list.append(k)
			correct_keys.append(temp_list)
		bad_list_keys = flatten(correct_keys)
		settings_to_download = {}
		for k, v in st.session_state.items():
			if k not in bad_list_keys:
				settings_to_download[k] = v
		return settings_to_download

	def _create_download_settings(self):
		# 1. StreamlitDownloadFunctions Settings Button
		settings_to_download = self._create_excluding_session_dictionary()
		# st.write(self.settings_to_download.keys())
		# st.write([val for val in settings_to_download.keys() if "button" in val])
		self.button_download = st.download_button(label="Download Session Settings",
		                                          data=json.dumps(settings_to_download, ensure_ascii=False, indent=4),
		                                          file_name=f"settings.json",
		                                          help="Click to load Current Settings")

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


class UploadSessionSettingControl:
	@staticmethod
	def autoload_session():
		autoload_session = AutoloadSession()
		autoload_session.autoload()

	@staticmethod
	def load_session_download():
		uploaded_session_file = st.file_uploader(
			label="Select the Settings File to be uploaded",
			help=AppHelp.uploaded_session_file_help,
			type=[".json"]
		)
		upload_session = UploadSessionSetting(uploaded_session_file)
		upload_session.show_session_view()
