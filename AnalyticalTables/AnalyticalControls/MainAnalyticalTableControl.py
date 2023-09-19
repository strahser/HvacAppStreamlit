
from SQL.SqlControl.SqlQueryViewTableControl import *
from SQL.SqlModel.SqlConnector import SqlConnector



class AnalyticalTableControl:
	"""read sql table for analytic"""

	def __init__(self, upload_layout: UploadLayout, connector=SqlConnector.conn_sql,key=""):
		self.upload_layout = upload_layout
		self.connector = connector
		self.key = key
		sql_view_table = SqlQueryViewTableControl(self.upload_layout, key=f"choose_group_table_or_sql{self.key}")
		sql_view_table.create_all_query_view()