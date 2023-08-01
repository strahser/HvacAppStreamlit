
from SqlDynamicCalculator.View.SQLCreateViewPanel import SQLCreateViewPanel
from SqlDynamicCalculator.Controls.SqlDynamicControl import *
from StaticData.AppConfig import MenuChapters


class InputDataControl:
	def __init__(self, upload_layout: UploadLayout, conn: object = SqlConnector.conn_sql) -> None:
		self.conn = conn
		self.upload_layout = upload_layout
		self.tabs_view = TabsViewControl(self.upload_layout)
		sql_dynamic = SqlDynamicControl(self.tabs_view)
		self.sql_query = sql_dynamic.create_sql_query()
		self.sql_config = SQLCreateViewPanel(self.sql_query, key=f"dynami {MenuChapters.analytics}")
		self.sql_config.show_sql_view_panel()