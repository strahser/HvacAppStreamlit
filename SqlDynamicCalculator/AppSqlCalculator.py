from SqlDynamicCalculator.View.SQLCreateViewPanel import SQLCreateViewPanel
from SqlDynamicCalculator.Controls.SqlDynamicControl import *
from StaticData.AppConfig import MenuChapters


def SqlDynamicCalculator(upload_layout: UploadLayout):
	tabs_view = TabsViewControl(upload_layout)
	tabs_view.show_tabs_view()
	sql_dynamic = SqlDynamicControl(tabs_view)
	sql_query = sql_dynamic.create_sql_query()
	sql_config = SQLCreateViewPanel(sql_query, key=f"dynamic {MenuChapters.analytics}")
	sql_config.show_sql_view_panel()
