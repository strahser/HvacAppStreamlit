import json
from collections import defaultdict

from Session.StatementConfig import StatementConstants
from Upload.LoadExcelBooks import LoadExcelBooks
from Upload.UploadView import *
from SQL.SqlModel.SqlConnector import *
from InputView.InputViewModel.SelectDataDBModel import SelectDataDBModel
from library_hvac_app.list_custom_functions import to_list


def without_keys(d: dict, keys: list[str]):
	keys = to_list(keys)
	return {k: v for k, v in d.items() if k not in keys}


class UploadLayout:
	def __init__(self, upload_view: UploadView, conn=SqlConnector.conn_sql) -> None:
		session_tables = st.session_state[StatementConstants.table_db]
		self.upload_view = upload_view
		self.connector = conn
		self._table_dict = defaultdict(list)
		self.table_dict = dict()
		self.json_file = None
		self.all_db_views = session_tables[StatementConstants.all_tables_view]
		self.table_dict.\
			update(without_keys(session_tables, StatementConstants.all_tables_view))

	def get_files_from_memory(self):
		if self.upload_view.update_db_button:
			self._table_dict = self._select_db_or_excel_update()
		if self.upload_view.file_json_upload:
			st.session_state[StatementConstants.json_polygons] = self._get_json_file_from_memory()
			self.json_file = st.session_state[StatementConstants.json_polygons]

	def _select_db_or_excel_update(self):
		if (self.upload_view.select_db_or_excel == StaticVariable.load_excel.value
				and self.upload_view.input_excel_sheet_uploader):
			load_excel_book = LoadExcelBooks(self._table_dict, connector=self.connector)
			_table_dict = load_excel_book.add_all_excel_book_sheets_to_db(self.upload_view.input_excel_sheet_uploader)
			return _table_dict

		elif self.upload_view.select_db_or_excel == StaticVariable.load_db.value and self.upload_view.upload_db:
			self._get_db_data()
			return {}

	def _get_json_file_from_memory(self):
		json_file = self.upload_view.file_json_upload.getvalue()
		data = json.loads(json_file)
		return data

	def _get_db_data(self):
		raw_text = str(self.upload_view.upload_db.read(), "utf-8")
		try:
			self.connector.cursor().executescript(raw_text)
			self.connector.commit()
		except Exception as e:
			st.warning(e)
