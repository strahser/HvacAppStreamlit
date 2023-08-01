from DashBoard.ExpressCharts.StaticDfView import StaticDfView
from DashBoard.ExpressCharts.StaticPivotDFView import StaticPivotDFView
from DashBoard.ExpressCharts.StreamlitExpressCharts import StreamlitExpressCharts
from DashBoard.ExpressCharts.StreamlitExpressChartsView import StreamlitExpressChartsView


class DFStaticTab:
	def __init__(self, table_name: str, key: str):
		self.table_name = table_name
		self.key = key
		self.character_df_view = StreamlitExpressChartsView(self.table_name, self.key)
		self.character_df_view.create_view_column_df_choosing()

	def create_static_view(self):
		static_df_view = StaticDfView(self.character_df_view, self.key)
		static_df_view.create_static_df_view()

	def create_pivot_df_view(self):
		pivot_df_view = StaticPivotDFView(self.character_df_view, self.key)
		pivot_df_view.create_pivot_dash()

	def create_dynamic_view(self, agg_func):
		express_chart = StreamlitExpressCharts(self.character_df_view, self.key, agg_func=agg_func)
		express_chart.create_plotly_dynamic_charts()
