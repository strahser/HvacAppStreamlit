import pandas as pd
import streamlit as st
from InsertTerminalsPandas.InputData.input import InputDataDF
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
from SQL.SQlTools.SqlOperations.SqlCRUDOperation import SqlCRUDOperation
from SQL.SqlModel.SqlConnector import SqlConnector
from library_hvac_app.streamlit_custom_functions import AggGridOptions


class DeviceCRUDView:
	def __init__(self, input_data_df: InputDataDF):
		self.con = SqlConnector.conn_sql
		self.col1, self.col2, self.col3 = st.columns(3)
		self.input_data_df = input_data_df

	@property
	def device_type_df(self) -> pd.DataFrame:
		try:
			# device_type_df = pd.read_sql(f"select * from {ColumnChoosing.device_type}", con=self.con)
			device_type = self.input_data_df.device_type
			return device_type
		except Exception as e:
			self.__exception_create(e)

	@property
	def devices_df(self) -> pd.DataFrame:
		try:
			# devices_df = pd.read_sql(f"select * from {ColumnChoosing.devices}", con=self.con)
			devices = self.input_data_df.devices
			return devices
		except Exception as e:
			self.__exception_create(e)

	def create_devices_db_view(self) -> list[str]:
		"""system names and devices agg table"""
		try:
			self.changed_column = self._create_device_filter_view()
			self.new_column_value = self._create_device_type_filter_view()
			self.id_column = self._create_id_filter_view()
			with st.sidebar:
				self.add_data_to_column_button = st.button("add data to column")
				st.button("update view")
			selected_types_data = AggGridOptions(self.devices_df)
			selected_types_data = selected_types_data.create_ag_selected_row_df("selected_rows")
			selected_types_data = pd.DataFrame(selected_types_data)
			if not selected_types_data.empty:
				selected_types_data = selected_types_data[ColumnChoosing.S_ID].to_list()
				selected_types_data = [str(val) for val in selected_types_data]
				if self.add_data_to_column_button:
					self.__add_data_to_column(selected_types_data, self)
				return selected_types_data
		except Exception as e:
			self.__exception_create(e)

	@staticmethod
	def __add_data_to_column(filtered_df: list, table_add_data_view):
		sql_operation = SqlCRUDOperation(ColumnChoosing.devices)
		sql_operation.add_data_to_column(filtered_df, table_add_data_view)

	def _create_id_filter_view(self) -> list[str]:
		with self.col3:
			_index = self.devices_df.columns.to_list().index(
				ColumnChoosing.S_ID) if ColumnChoosing.S_ID in self.devices_df.columns else 0
			st.subheader('Choose  ID column')
			id_column = st.selectbox('select id column',
			                         self.devices_df.columns,
			                         index=_index,
			                         key='select id column')
		return id_column

	def _create_device_filter_view(self) -> list[str]:
		try:
			system_type_df = list(self.input_data_df.system_dictionary.keys())
			with self.col1:
				st.subheader('Choose  System Options')
				selected_system_columns_names = st.selectbox('select system type columns',
				                                             system_type_df,
				                                             index=0,
				                                             key='select system type columns')
				return selected_system_columns_names
		except Exception as e:
			self.__exception_create(e)

	def _create_device_type_filter_view(self) -> list[str]:
		device_type = self.device_type_df["type_index"].to_list()
		device_type.append("")
		with self.col2:
			st.subheader('Choose  Device Options')
			selected_device_type_names = st.selectbox('select device type column',
			                                          device_type,
			                                          index=0,
			                                          key='select device type column')
		return selected_device_type_names

	@staticmethod
	def __exception_create(e):
		st.warning(e)
		st.empty()
		return None
