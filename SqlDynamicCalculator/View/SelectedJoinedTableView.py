import sqlite3
import streamlit as st
import pandas as pd
from SqlDynamicCalculator.CategoryDb import TableNameConstants


class SelectedJoinedTableView:

	def __init__(self, key: str, table_selected_dict: dict, conn: sqlite3.Connection, number_of_tables: int = 1):
		"""Table left,right,index,how to join view"""
		with st.expander(f"__Select Options for {key}__"):
			st_columns = st.columns(5)
			if "main" in key:
				self.joined_table_name_left = st_columns[0].selectbox(f"Left Table {key}",
				                                                      list(table_selected_dict.values()),
				                                                      key=f"table_name_left_table_name {key}")
				if number_of_tables > 1:
					self.how_to_join = st_columns[1].selectbox(f"How to join Table {key}",
					                                           TableNameConstants.how_to_join,
					                                           key=f"how_to_join {key}")
			else:
				self.joined_table_name_left = st_columns[0].selectbox(f"Select Left Table Index {key}",
				                                                      list(table_selected_dict.values()),
				                                                      key=f"table_name_left_table_name {key}")
				
				self.joined_table_name_right = st_columns[2].selectbox(f"Right Table {key}",
				                                                       list(table_selected_dict.values()),
				                                                       key=f"table_name_right_table_name {key}")
				
				self.left_join_index = st_columns[1].selectbox(f"Left Table Index {self.joined_table_name_left}",
				                                               pd.read_sql(
					                                               f"select * from {self.joined_table_name_left}",
					                                               conn)
				                                               .columns.to_list(),
				                                               key=f"left_table_index_for_join {key}")
				
				self.right_join_index = st_columns[3].selectbox(f"Right Table Index {self.joined_table_name_right}",
				                                                pd.read_sql(
					                                                f"select * from {self.joined_table_name_right}",
					                                                conn)
				                                                .columns.to_list(),
				                                                key=f"right_table_index_for_join {key}")
				self.how_to_join = st_columns[4].selectbox(f"How to join Table {key}",
				                                           TableNameConstants.how_to_join,
				                                           key=f"how_to_join {key}")
