from InputView.InputView import InputView
from Session.StatementConfig import StatementConstants
from Session.UpdateDbSession import UpdateDbSession
from Upload.UploadLayout import UploadLayout
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd
import streamlit as st


class InputViewControl:
	def __init__(self, upload_layout: UploadLayout, key, connector=SqlConnector.conn_sql):
		self.input_df = pd.DataFrame()
		self.all_books = upload_layout.table_dict
		self.sheet_name = None
		self.connector = connector
		self.key = key
		self.input_view = InputView(all_books=self.all_books, all_views=upload_layout.all_db_views, key=self.key)

	def create_input_view(self):
		self.sheet_name = self.input_view.select_books_or_views_view()
		all_tables_session = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		all_views_session = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		UpdateDbSession.Update_sql_sessionData()

		if (
				self.sheet_name in all_tables_session
				or self.sheet_name in all_views_session
		):
			try:
				self.input_df = pd.read_sql(f"select *  from {self.sheet_name}", con=self.connector)
				return self.input_df
			except Exception as e:
				st.write(e)
				return pd.DataFrame()
		else:
			self.input_df = pd.DataFrame()
			return self.input_df
