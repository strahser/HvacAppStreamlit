import collections
import json
import streamlit as st
from streamlit import session_state as _state
from Session.StatementConfig import StatementConstants, SettingConfig


def condition_session_save(loading_file: dict, save=True) -> dict:
	""""button" not in key and "file_uploader" not in key and MenuChapters Scheme in key"""

	def _create_condition_list(key: str) -> bool:
		"""create condition for session save load"""
		key_not_in_exclude_list = key not in SettingConfig.excluding_list
		key_not_a_button = "button" not in key
		key_in_menu_keys = _state.get(StatementConstants.mainHydralitMenuComplex) in key
		return key_not_in_exclude_list and key_not_a_button and key_in_menu_keys

	for k, v in st.session_state.items():
		""" update upload file or session """

		_condition_list = _create_condition_list(k)
		if _condition_list and save:
			loading_file.update({k: v})
		elif _condition_list and not save:
			_state.update({
				key: value
				for key, value in loading_file.items()
			})
	return loading_file


class AutoloadSession:
	def __init__(self):
		self.loading_file = self._add_session_loading_file()

	@staticmethod
	def _add_session_loading_file():
		return _state[StatementConstants.loading_file]

	def autoload(self):
		if _state[StatementConstants.previous_view] == _state[StatementConstants.mainHydralitMenuComplex]:
			self._save_json()
		elif _state[StatementConstants.previous_view] != _state[StatementConstants.mainHydralitMenuComplex]:
			self._load_json()

	def _save_json(self):
		condition_session_save(self.loading_file, save=True)

	def _load_json(self):
		condition_session_save(self.loading_file, save=False)



