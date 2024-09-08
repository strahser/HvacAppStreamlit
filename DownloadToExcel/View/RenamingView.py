from InputView.InputView import InputView
import pandas as pd
import streamlit as st


class RenamingView:
	def __init__(self, input_view: InputView, con, rename_columns_tab):
		self.input_view = input_view
		self.con = con
		self.rename_columns_tab = rename_columns_tab

	def get_renaming_columns_view(self) -> dict:
		with self.rename_columns_tab:
			st.markdown("#### Select excel list for renaming sheets columns")
			selected_sheet = self.input_view.select_books_or_views_view()
			renamed_df = pd.read_sql(f"select * from {selected_sheet}", con=self.con)
			col = st.columns(4)
			column_keys = col[0].selectbox("Choose Columns Keys", renamed_df.columns, key="renaming key column")
			column_values = col[1].selectbox("Choose Columns Values", renamed_df.columns, key="renaming value column")
			keys = renamed_df[column_keys].tolist()
			values = renamed_df[column_values].tolist()
			dict_df = dict(zip(keys, values))
			st.write(renamed_df)
		return dict_df
