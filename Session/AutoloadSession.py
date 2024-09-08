import streamlit as st
from streamlit import session_state as _state
from Session.StatementConfig import StatementConstants, SettingConfig


class AutoloadSession:
	@staticmethod
	def autoload():
		if _state[StatementConstants.previous_view] == _state[StatementConstants.mainHydralitMenuComplex]:
			AutoloadSession.condition_session_save(_state[StatementConstants.loading_file], "save")
		if _state[StatementConstants.previous_view] != _state[StatementConstants.mainHydralitMenuComplex]:
			AutoloadSession.condition_session_save(_state[StatementConstants.loading_file], "load")

	@staticmethod
	def condition_session_save(loading_file: dict, save_or_load) -> dict:
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
			if _condition_list and save_or_load == "save":
				loading_file.update({k: v})
			elif _condition_list and save_or_load == "load":
				_state.update({key: value for key, value in loading_file.items()})
		return loading_file
