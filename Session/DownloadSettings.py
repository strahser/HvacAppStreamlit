import numpy as np
import json
from Session.StatementConfig import StatementConstants, SettingConfig
from library_hvac_app.list_custom_functions import flatten
from json import encoder
import streamlit as st
encoder.FLOAT_REPR = lambda o: format(o, '.2f')


class NumpyEncoder(json.JSONEncoder):
	""" Custom encoder for numpy data types """

	def default(self, obj):
		if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
		                    np.int16, np.int32, np.int64, np.uint8,
		                    np.uint16, np.uint32, np.uint64)):

			return int(obj)

		elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
			return float(obj)

		elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
			return {'real': obj.real, 'imag': obj.imag}

		elif isinstance(obj, (np.ndarray,)):
			return obj.tolist()

		elif isinstance(obj, (np.bool_)):
			return bool(obj)

		elif isinstance(obj, (np.void)):
			return None

		return json.JSONEncoder.default(self, obj)


class DownloadSettings:
	def __init__(self):
		st.subheader("Download settings")
		self._create_download_settings()

	@staticmethod
	def _create_download_settings():
		# 1. StreamlitDownloadFunctions Settings Button
		settings_to_download = DownloadSettings._create_excluding_session_dictionary()
		st.download_button(label="Download Session Settings",
		                   data=json.dumps(
			                   settings_to_download,
			                   ensure_ascii=False,
			                   indent=4,
			                   cls=NumpyEncoder
		                   ),
		                   file_name=f"settings.json",
		                   help="Click to load Current Settings")

	@staticmethod
	def _create_excluding_session_dictionary():
		excluding_list = SettingConfig.excluding_list
		all_keys = st.session_state.keys()
		correct_keys = []
		for excl_val in excluding_list:
			temp_list = []
			for k in all_keys:
				if excl_val in k:
					temp_list.append(k)
			correct_keys.append(temp_list)
		bad_list_keys = flatten(correct_keys)
		settings_to_download = {}
		for k, v in st.session_state.items():
			if k not in bad_list_keys:
				settings_to_download[k] = v
		return settings_to_download
