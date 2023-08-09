import streamlit as st
from InputView.InputViewModel.SelectDataDBModel import SelectDataDBModel
import pandas as pd
from StaticData.AppConfig import StaticVariable
from Session.StatementConfig import StatementConstants
from library_hvac_app.list_custom_functions import to_list


class InputView:

	def __init__(self, all_books: dict, key, all_views: list[str]):
		"""create table  and view choosing options"""
		self.selected_excel_books = None
		self.selected_excel_sheet = None
		self.key = key
		self.all_books = all_books
		self.all_views = all_views
		self.columns = st.columns(4)
		self.index_book = 0
		self.index_sheet = 0

	def select_books_or_views_view(self) -> None:
		self.selected_excel_sheet = self._create_radio_button()
		return self.selected_excel_sheet

	def _get_category_json_view(self) -> str:
		all_tables = st.session_state[StatementConstants.create_json]
		if all_tables:
			df = pd.DataFrame(all_tables.values())
			df = df.groupby([StatementConstants.category_name])[StatementConstants.view_name].agg(list).to_dict()
			category_stat = st.session_state[StatementConstants.category_dictionary]
			category_stat.update(df)
			with self.columns[0]:
				selected_excel_book = st.selectbox("Select Excel book",
				                                   df.keys(),
				                                   key=f"{self.key} selected_excel_book",
				                                   )
			with self.columns[1]:
				selected_excel_sheet = st.selectbox("Select Excel sheet",
				                                    list(df[selected_excel_book]),
				                                    key=f"{self.key} selected_excel_sheet",
				                                    )
				self.selected_excel_books = selected_excel_book
			return selected_excel_sheet

	def _create_radio_button(self):

		selected_option = st.radio("Select Input table or Input view",
		                           ("Show Tables", "Show Views", "Show Category"),
		                           key=f"{self.key} selected_option")
		if selected_option == "Show Tables" and self.all_books:
			return self.get_selected_sheet()
		if selected_option == "Show Views" and self.all_views:
			return self._select_db_view_sheet()
		if selected_option == "Show Category":
			return self._get_category_json_view()

	def get_selected_sheet(self):
		self.selected_excel_books = self._select_excel_book()
		selected_sheet = self._select_excel_sheet(self.selected_excel_books)
		return selected_sheet

	def _select_excel_book(self, ):
		with self.columns[0]:
			selected_excel_book = st.selectbox(
				"Select Excel Book",
				self.all_books.keys(),
				key=f"{self.key} selected_excel_books"
			)
			return selected_excel_book

	def _select_excel_sheet(self, selected_excel_books):
		with self.columns[1]:
			selected_excel_sheet = st.selectbox("Select Excel Sheet",
			                                    to_list(self.all_books[selected_excel_books]),
			                                    key=f"{self.key} selected_excel_sheet",
			                                    )
			return selected_excel_sheet

	def _select_db_view_sheet(self):
		with self.columns[0]:
			selected_excel_sheet = st.selectbox("Select Db Views",
			                                    self.all_views,
			                                    key=f"{self.key} selected_view",
			                                    )
			self.selected_excel_books = StatementConstants.all_tables_view
			return selected_excel_sheet
