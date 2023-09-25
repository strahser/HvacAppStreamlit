import pandas as pd
import streamlit as st
import numpy as np
from streamlit_modal import Modal

from InputView.InputViewControl import InputViewControl
from SQL.SqlModel.SqlConnector import SqlConnector
from Upload.UploadLayout import UploadLayout


# pip install orjson


def numpy_int64_converted(value_list: list) -> list:
	return [int(val) if isinstance(val, np.int64) else val for val in value_list]


def create_modal_window(upload_layout, open_modal_button: bool, key, index=0):
	modal = Modal("Upload DB Data", key=key, padding=100)
	if open_modal_button:
		modal.open()
	if modal.is_open():
		with modal.container():
			_create_input_sql_tools_view(upload_layout, key, index)


def _create_input_sql_tools_view(upload_layout, key, index=0):
	input_view_control = InputViewControl(upload_layout, key)
	input_view_control.create_input_view()
	input_df = input_view_control.input_df
	table_name = input_view_control.sheet_name
	st.write(table_name, index)
	return input_df, table_name


class EditableDataFrameColumnsData:
	columns_width = [2, 2, 2]
	columns_names = [
		"Combobox Data Name",
		"Data Requirements?",
	]

	@staticmethod
	def add_to_session() -> None:
		if "tables name" not in st.session_state:
			st.session_state["tables name"] = {}


class EditableDataFrameView:

	def __init__(self, table_name_default, upload_layout: UploadLayout, key: str):
		self.columns_names = EditableDataFrameColumnsData.columns_names
		self.table_name_default = table_name_default
		self.upload_layout = upload_layout
		self.key = key
		self.input_df = pd.read_sql(f"select * from {table_name_default}", con=SqlConnector.conn_sql)
		self.combobox_names = {}
		st.subheader("Choose Combobox Settings")
		min_col=st.columns(3)
		self.min_combobox = min_col[0].number_input("Number of combobox", step=1, min_value=0)
		self.columns = st.columns(EditableDataFrameColumnsData.columns_width)

	def create_layout(self) -> pd.DataFrame:
		if self.min_combobox > 0:
			self._create_headers_of_table()
			for en in range(self.min_combobox):
				columns = st.columns(EditableDataFrameColumnsData.columns_width)
				selected_column = self._select_column_for_combobox(columns, en)
				required = self._can_data_be_empty(columns, en)
				config_selected_column = self._config_selected_column(selected_column, required)
				self.combobox_names.update(config_selected_column)
			df_editable = st.data_editor(
				data=self.input_df,
				num_rows="dynamic",
				column_config=self.combobox_names,
				key=f"{self.key} df_editable"
			)
			return df_editable

	def _create_headers_of_table(self):
		for en, val in enumerate(self.columns_names):
			# create headers of table
			self.columns[en].write(val)

	def _show_selected_table(self, en) -> str:
		# show selected table
		with self.columns[0]:
			return st.text_input(
				"Select combobox column",
				label_visibility="collapsed",
				value=self.table_name_default,
				disabled=True,
				key=f"selected_table {en}"
			)

	def _select_column_for_combobox(self,columns,  en) -> str:
		# select column for combobox
		with columns[0]:
			return st.selectbox(
				"Select combobox column",
				self.input_df.columns,
				label_visibility="collapsed",
				key=f"selected_column {en}"
			)

	def _can_data_be_empty(self,columns,  en) -> bool:
		# can data be empty data
		with columns[1]:
			return st.checkbox("Is not Empty?", key=f"is_requirement {en}",
			                   label_visibility="collapsed", value=True)

	def _config_selected_column(self, selected_column: str, required: bool) -> dict:
		return {
			selected_column: st.column_config.SelectboxColumn(
				selected_column,
				width="medium",
				options=numpy_int64_converted(self.input_df[selected_column].dropna().unique()),
				required=required
			),
		}

	def _load_another_data_source(self, en: int, col_conf: dict):
		# load another data source
		with self.columns[3]:
			data_button = st.checkbox("Another Table", key=f"get view button {en}")
		with self.columns[4]:
			if data_button:
				input_df_, table_name_ = _create_input_sql_tools_view(self.upload_layout, f"{self.key} view{en}", en)
				confirm_button = st.button("confirm", key=f"{self.key} confirm {en}")
				if confirm_button:
					st.session_state["tables name"].update({en: table_name_})
		st.write(st.session_state["tables name"])
		self.combobox_names.update(col_conf)


def create_editable_df(table_name_default, upload_layout, key)->pd.DataFrame:
	try:
		df = EditableDataFrameView(table_name_default, upload_layout, key)
		df_editable = df.create_layout()
		return df_editable
	except Exception as e:
		st.warning(f" please check combobox column data {e}")
