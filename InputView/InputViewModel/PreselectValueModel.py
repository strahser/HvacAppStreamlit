import streamlit as st


class PreselectValueModel:
	def __init__(self, table_dict: dict):
		"""get default book and sheet index"""
		self.index_sheet = 0
		self.index_book = 0
		self.table_dict = table_dict
		self.all_sheets = False

	def preselect_data(self, search_sheet: str = None) -> bool:
		"search list in dictionary keys and values list of all necessary  value_list"
		if search_sheet:
			for book, sheets in self.table_dict.items():
				condition_books = book == search_sheet and book != "All Sheets"
				if condition_books:
					index_book = [i for i, j in enumerate(self.table_dict.keys()) if j == book]
					self.index_book = index_book[0] if index_book else 0
					self.all_sheets = True
				else:
					for sheet in sheets:
						if sheet == search_sheet:
							index_book = [i for i, j in enumerate(self.table_dict.keys()) if j == book]
							index_sheet = [i for i, j in enumerate(sheets) if j == sheet]
							self.index_book = index_book[0] if index_book else 0
							self.index_sheet = index_sheet[0] if index_sheet else 0
							self.all_sheets = False

