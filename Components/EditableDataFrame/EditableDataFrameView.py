import pandas as pd
import streamlit as st
import numpy as np
from streamlit_modal import Modal

from InputView.InputViewControl import InputViewControl
from SQL.SqlModel.SqlConnector import SqlConnector


# pip install orjson


def numpy_int64_converted(value_list: list) -> list:
	return [int(val) if isinstance(val, np.int64) else val for val in value_list]


def create_modal_window(upload_layout, open_modal_button:bool, key,index=0):
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


def create_editable_df(table_name_default, upload_layout, key):
	input_df = pd.read_sql(f"select * from {table_name_default}", con=SqlConnector.conn_sql)
	st.subheader("Choose Combobox Settings")
	columns_ = st.columns(3)
	min_combobox = columns_[0].number_input("Number of combobox", step=1, min_value=0)
	combobox_names = {}
	if min_combobox > 0:
		columns_width = [2, 2, 1, 2]
		columns_names = ["Data Table Name", "Combobox Data Name", "Data Requirements?",
		                 "Choose Another data Source"]
		columns = st.columns(columns_width)
		for en, val in enumerate(columns_names):
			columns[en].write(val)
		for en in range(min_combobox):
			columns = st.columns(columns_width)
			with columns[0]:
				selected_table = st.text_input(
					"Select combobox column",
					label_visibility="collapsed",
					value=table_name_default,
					disabled=True,
					key=f"selected_table {en}"
				)
			with columns[1]:
				selected_column = st.selectbox(
					"Select combobox column",
					input_df.columns,
					label_visibility="collapsed",
					key=f"selected_column {en}"
				)
			with columns[2]:
				is_requirement = st.checkbox("Data requirement?", key=f"is_requirement {en}",
				                             label_visibility="collapsed", value=True)
			col_conf = {
				selected_column: st.column_config.SelectboxColumn(
					selected_column,
					width="medium",
					options=numpy_int64_converted(input_df[selected_column].dropna().unique()),
					required=is_requirement
				),
			}
			with columns[3]:
				data_button = st.button("Another Table", key=f"get view button {en}")
			with columns[0]:
				if data_button:
					_create_input_sql_tools_view(upload_layout, key, en)
			combobox_names.update(col_conf)
	try:
		df_editable = st.data_editor(
			data=input_df,
			num_rows="dynamic",
			column_config=combobox_names
		)
	except Exception as e:
		st.warning(f" please check combobox column data {e}")
