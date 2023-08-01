import numpy as np
import pandas as pd

from SQL.SqlModel.SqlConnector import SqlConnector
import streamlit as st


class StreamlitExpressChartsView:
	def __init__(self, table_name: str, key: str):
		self.select_agg = None
		self.select_subgroup = None
		self.select_keys_y = None
		self.select_keys_x = None
		self.table_name = table_name
		self.key = key
		self.header = f"Charts of {self.table_name.replace('_', ' ').title()}"
		self.df = pd.read_sql(f"select * from {self.table_name}", con=SqlConnector.conn_sql).fillna("")
		self.agg_data = ['sum', 'max', 'mean']

	def create_view_column_df_choosing(self):
		numeric_columns = self.df.select_dtypes(include=np.number).columns.tolist()
		col = st.columns(4)
		with col[0]:
			st.write(f"#### Select Categorical Columns")
			self.select_keys_x = st.selectbox(self.header, self.df.columns,
			                                  key=f"{self.key} select_keys_x {self.table_name}",
			                                  label_visibility="collapsed")
		with col[1]:
			st.write(f"#### Select Number Columns")
			self.select_keys_y = st.selectbox(self.header, self.df.columns,
								key=f"{self.key} select_keys_y {self.table_name}",
								index=numeric_columns[0],
								label_visibility="collapsed")
		with col[2]:
			st.write(f"#### Select Subgroup Columns")
			self.select_subgroup = st.multiselect(self.header, self.df.columns,
			                                      key=f"{self.key} select_subgroup {self.table_name}",
			                                      label_visibility="collapsed")
		with col[3]:
			st.write(f"#### Select Aggregate Columns")

			self.select_agg = st.multiselect(self.header, self.agg_data,
			                                 default=self.agg_data[0],
			                                 key=f"{self.key}  {self.table_name}",
			                                 label_visibility="collapsed")
