
from Session.AutoloadSession import AutoloadSession
import streamlit as st


class ManualSaveLoadSession(AutoloadSession):
	def __init__(self):
		self._view_create()
		if self.save_session_button:
			self._save_json()
		if self.load_session_button:
			self._load_json()

	def _view_create(self):
		self.save_session_button = st.button("Save Session?")
		self.load_session_button = st.button("Load Session?")