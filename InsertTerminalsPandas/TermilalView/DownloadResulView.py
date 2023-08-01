import streamlit as st

class DownloadResulLayout:
	def __init__(self, excel_file, json_file):
		self.excel_file = excel_file
		self.json_file = json_file

	def create_download_layout(self):
		st.subheader('Downloads')
		st.download_button(label='📥  Download excel',
		                   data=self.excel_file,
		                   file_name="concat_df_data.xlsx", )
		st.download_button(label='📥 Download json',
		                   data=self.json_file,
		                   file_name="json_data.json", )
