from InputView.InputView import InputView
from DownloadToExcel.View.RenamingView import RenamingView

import streamlit as st
from DownloadToExcel.View.TabsView import TabsView
from DownloadToExcel.Control.BalanceControl import BalanceControl
from Session.StatementConfig import StatementConstants
from library_hvac_app.StreamlitDownloadFunctions.DownloadExcel import download_excel_sheets
import pandas as pd
from SQL.SqlModel.SqlConnector import SqlConnector
from st_aggrid import AgGrid, GridOptionsBuilder


class DownloadView:
	def __init__(self, input_view: InputView, con=SqlConnector.conn_sql):
		self.con = con
		self.input_view = input_view
		self.tables_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
		self.views_name = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
		self.all_tables_names = self.tables_name + self.views_name
		self.tabs = TabsView()
		with self.tabs.download_view_tab:
			self.download_tab, self.rename_columns_tab = st.tabs(["Download", "Rename Columns"])

	def get_balance_view(self, balance_control: BalanceControl):
		with self.tabs.balance_view_tab:
			balance_control()

	def get_download_view(self):
		with self.download_tab:
			st.markdown("#### Select sheets for download")
			self._create_select_view()

	def _create_select_view(self):
		select_view_or_tables_names = st.radio("Select Option", ["Table DB", "View DB", "All"])
		if select_view_or_tables_names == "All":
			return self._download_names_select(self.all_tables_names)
		if select_view_or_tables_names == "Table DB":
			return self._download_names_select(self.tables_name)
		if select_view_or_tables_names == "View DB":
			return self._download_names_select(self.views_name)

	def _create_df_list_from_sql(self, selected_tables_names) -> list[pd.DataFrame]:
		df_list = [
			pd.read_sql(f"select * from {name}", con=self.con) for name in selected_tables_names
			if selected_tables_names
		]
		return df_list

	def _download_names_select(self, table_names: list[str]):
		rename_columns = st.checkbox("Rename Tables Columns and Table Name?")
		selected_tables_names = st.multiselect("Select Tables for download", table_names, default=table_names)
		if rename_columns:
			selected_df = self._create_df_list_from_sql(table_names)
			renaming_view = RenamingView(self.input_view, self.con, self.rename_columns_tab)
			renamed_dict = renaming_view.get_renaming_columns_view()
			rename_df = [df.rename(renamed_dict, axis='columns') for df in selected_df]
			with self.rename_columns_tab:
				renamed_sheet_dict = self._create_session_for_renamed_editable_table()
				st.session_state["df_sheet_view"] = {"Old Table Name": self.old_names.tolist(),
				                                     "New Table Name": self.new_names.tolist()}
				download_excel_sheets(rename_df, selected_tables_names, renamed_sheet_dict=renamed_sheet_dict)
		else:
			download_excel_sheets(self._create_df_list_from_sql(table_names), selected_tables_names)

	def _create_session_for_renamed_editable_table(self):
		if "df_sheet_view" not in st.session_state:
			st.session_state["df_sheet_view"] = {"Old Table Name": self.tables_name, "New Table Name": self.tables_name}
		st.markdown("### Enter new list name ###")
		df = pd.DataFrame(st.session_state["df_sheet_view"])
		gb = GridOptionsBuilder.from_dataframe(df)
		gb.configure_default_column \
			(enablePivot=True,
			 enableValue=True,
			 enableRowGroup=True,
			 editable=True,
			 groupable=True,
			 min_column_width=10
			 )
		gridoptions = gb.build()
		agg = AgGrid(df, gridOptions=gridoptions)
		new_df = agg['data']
		self.old_names = new_df["Old Table Name"]
		self.new_names = new_df["New Table Name"]
		renamed_sheet_dict = dict(zip(self.old_names, self.new_names))
		return renamed_sheet_dict
