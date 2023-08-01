import streamlit

from SQL.SqlModel.SqlConnector import SqlConnector
from SQL.SqlView.AceEditorView import AceEditorView
from SQL.SqlView.CopyToClipBoardView import CopyToClipBoardView


class QueryInputStaticTextView:
	def __init__(self, connector=SqlConnector.conn_sql, key="Static SQL"):
		self.query_input = None
		self.connector = connector
		self.key = key

	def create_input_text_query(self):
		self.query_input = AceEditorView()



