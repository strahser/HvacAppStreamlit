from SQL.SqlModel.SqlConnector import SqlConnector
from Session.StatementConfig import StatementConstants
import pandas as pd


import streamlit as st


class SqlDFLoad:
	def __init__(self):
		self.conn = SqlConnector

	def get_all_db_tables(self):
		return pd.read_sql_query(
			"SELECT name FROM sqlite_master WHERE type='table';", con=self.conn
		)

	def get_balance_load_df_table(self):
		return pd.read_sql_query(
			f"select * from {StatementConstants.balance_load_columns_table}", con=self.conn
		)


class ConfigModel:
	def __init__(self):
		self.conn = SqlConnector.conn_sql

	@staticmethod
	def create_balance_load_columns_table(conn =SqlConnector.conn_sql):
		conn.cursor().viewer_execute(
			f"""
		CREATE TABLE IF NOT EXISTS {StatementConstants.balance_load_columns_table} (
		input_excel_sheet TEXT UNIQUE,
		df_new_table_name TEXT UNIQUE,
		balance_type_selected TEXT, 
		df_joined_column_name TEXT,
		df_total_sum_column_name TEXT,
		df_new_sum_column_name TEXT						
		)
			"""
		)
		conn.commit()

	@staticmethod
	def add_balance_data_to_table(
	                      input_excel_sheet: str,
	                      df_new_table_name: str,
	                      balance_type_selected: str,
	                      df_joined_column_name: str,
	                      df_total_sum_column_name: str,
	                      df_new_sum_column_name: str,
							conn=SqlConnector.conn_sql
	                      ):
		q = f"""select input_excel_sheet from {StatementConstants.balance_load_columns_table}"""
		col = pd.read_sql_query(q, con=conn)['input_excel_sheet'].to_list()

		if str(input_excel_sheet) not in col:
			conn.cursor().viewer_execute(
				f'INSERT INTO {StatementConstants.balance_load_columns_table} values(?,?,?,?,?,?)', (
					input_excel_sheet,
					df_new_table_name,
					balance_type_selected,
					df_joined_column_name,
					df_total_sum_column_name,
					df_new_sum_column_name,
				)

			)
			conn.commit()
			result_of_db_adding = "record add to db"
			return result_of_db_adding

		else:
			result_of_db_adding = f" {df_new_table_name} not unique"
			return result_of_db_adding
