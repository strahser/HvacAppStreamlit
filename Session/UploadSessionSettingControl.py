from Session.UploadSessionSetting import UploadSessionSetting
from StaticData.AppHelp import AppHelp
import streamlit as st


class UploadSessionSettingControl:

	@staticmethod
	def load_session_download():
		uploaded_session_file = st.file_uploader(
			label="Select the Settings File to be uploaded",
			help=AppHelp.uploaded_session_file_help,
			type=[".json"]
		)
		upload_session = UploadSessionSetting(uploaded_session_file)
		upload_session.show_session_view()