import streamlit as st
import pandas as pd


class CopyToClipBoardView:
	def __init__(self, query_input, connector, key):
		self.copy_to_clipboard = st.button("Copy DB to Clipboard", key=f"{key} copy_to_clipboard button", on_click=self._copy_df_to_clipboard)
		self.query_input = query_input
		self.connector = connector

	def _copy_df_to_clipboard(self):
		try:
			res = pd.read_sql_query(self.query_input, con=self.connector)
			res.to_clipboard()
		except Exception as e:
			st.warning(e)
			res = None
		return res
