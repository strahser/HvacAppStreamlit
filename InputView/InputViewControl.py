from InputView.InputView import InputView
from Session.StatementConfig import StatementConstants
from Upload.UploadLayout import UploadLayout
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd
import streamlit as st


class InputViewControl:
	def __init__(self, upload_layout: UploadLayout, key, connector=SqlConnector.conn_sql):
		self.all_books = upload_layout.table_dict
		self.connector = connector
		self.key = key
		self.input_view = InputView(self.all_books,all_views=upload_layout.all_db_views, key=self.key)

	def create_input_view(self, index_book=0, index_sheet=0):
		self.input_view.index_book = index_book
		self.input_view.index_sheet = index_sheet
		self.sheet_name = self.input_view.select_books_or_views_view()
		if (
				self.sheet_name in st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
				or self.sheet_name in st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		):
			self.input_df = pd.read_sql(f"select *  from {self.sheet_name}", con=self.connector)
			return self.input_df
		else:
			self.input_df = pd.DataFrame()
			return self.input_df
