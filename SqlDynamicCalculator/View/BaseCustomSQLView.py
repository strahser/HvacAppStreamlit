import pandas as pd
import streamlit as st
from SQL.SqlModel.SqlConnector import SqlConnector


class BaseCustomSQLView:
	def __init__(self, table_dictionary: dict[str, str], conn=SqlConnector.conn_sql):
		self.conn = conn
		self.table_dictionary = table_dictionary
		self.custom_function = st.text_input("Enter Custom Expiration")
		with st.expander(f"Select Options for Custom Function"):
			st_columns = st.columns(4)
			self.select_table_name = st_columns[0].selectbox(
				f"Select Table", list(self.table_dictionary.values()
				                      )
			)
			self.select_table_columns = st_columns[1].selectbox(f"Select Table Columns {self.select_table_name}",
			                                                    pd.read_sql(
				                                                    f"select * from {self.select_table_name}",
				                                                    self.conn)
			                                                    .columns.to_list(),
			                                                    )
			st.text(f""" {self.select_table_columns} """)
