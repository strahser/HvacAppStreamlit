import os
import json
import pandas as pd
from collections import defaultdict
from Session.StatementConfig import StatementConstants
from Upload.UploadView import *

from dataclasses import dataclass, field


class LoadExcelBooks:
	def __init__(self, table_dict: dict[str, list], connector):
		"""load excel"""
		self.table_dict = table_dict
		self.connector = connector

	def add_all_excel_book_sheets_to_db(self, excel_books: st.file_uploader) -> dict:
		"""create sheet tree in session"""
		for book in excel_books:
			book_name = os.path.splitext(str(book.name))[0]
			book = pd.read_excel(book, engine="openpyxl", sheet_name=None)
			for sheet_name, sheet in book.items():
				sheet.to_sql(sheet_name, if_exists='replace', con=self.connector, index=False)
				self.table_dict[book_name].append(sheet_name)
			st.session_state[StatementConstants.table_db].update(self.table_dict)
		return self.table_dict
