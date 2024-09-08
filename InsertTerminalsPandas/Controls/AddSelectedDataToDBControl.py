import pandas as pd
import streamlit as st

from SQL.SqlModel.SqlConnector import SqlConnector
from InsertTerminalsPandas.Static.DevicePropertiesName import DevicePropertiesName
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing


class AddSelectedDataToDBControl:
	def __init__(self,conn = SqlConnector.conn_sql):
		self.conn = conn
		self.cur = self.conn.cursor()

	def _create_table(self):
		default_columns = tuple(
			column_name for column_name in DevicePropertiesName.device_property_columns_names)
		with self.conn:
			self.cur.execute(f"""
			 CREATE TABLE IF NOT EXISTS device_type {default_columns}""")

	def add_device_data_new_row_to_db(self, class_instance, new_type_index=None):
		self._create_table()
		query_columns = [str(val) for val in DevicePropertiesName.device_property_columns_names]
		query_values = [str(getattr(class_instance, val)) for val in DevicePropertiesName.device_property_columns_names]

		if new_type_index:
			query_values_ = [
				f"'{new_type_index}'" if col == ColumnChoosing.type_index else f"'{val}'" for col, val in
				zip(query_columns, query_values)
			]
			query = f"""INSERT  INTO device_type ({", ".join(query_columns)}) VALUES ({",".join(query_values_)}) """
			self._commit_exception(query)
		else:
			joined_text = [f"{x} = '{y}'" for x, y in zip(query_columns, query_values)]
			zip_data = ''.join(','.join(joined_text))
			query = f"""UPDATE device_type SET {zip_data} WHERE {ColumnChoosing.type_index} = '{class_instance.type_index}'"""
			self._commit_exception(query)

	def _commit_exception(self, query):
		try:
			self.cur.execute(query)
			st.success("DB Updated")
			self.conn.commit()
			st.write(pd.read_sql("select * from device_type", con=self.conn))

		except Exception as e:
			st.warning(f"Can not update DB,{e}")
