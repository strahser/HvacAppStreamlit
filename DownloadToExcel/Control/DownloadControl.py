import sqlite3
from io import StringIO

from DownloadToExcel.View.DownloadView import *
from Upload.UploadLayout import UploadLayout
from InputView.InputView import InputView
from StaticData.AppConfig import MenuChapters
from SQL.SqlModel.SqlConnector import SqlConnector


class DownloadControl:
	def __init__(self, upload_layout: UploadLayout, con=SqlConnector.conn_sql):
		self.con = con
		self.upload_layout = upload_layout
		input_view = InputView(
			self.upload_layout.table_dict,
			all_views=self.upload_layout.all_db_views,
			key=MenuChapters.download)
		download_view = DownloadView(input_view)
		download_view.get_balance_view(BalanceControl)
		download_view.get_download_view()
		self.download_sqlite_db()

	@staticmethod
	def download_sqlite_db():
		# Read database to tempfile
		con = SqlConnector.conn_sql
		tempfile = StringIO()
		for line in con.iterdump():
			tempfile.write('%s\n' % line)
		tempfile.seek(0)

		btn = st.download_button(
			label="Download db file",
			data=tempfile.getvalue(),
			file_name="damp_db.sql",
			mime="application/octet-stream")