from DashBoard.ExpressCharts import StreamlitExpressChartsView


class _TableControl:
	def __init__(self, express_chart_view: StreamlitExpressChartsView, key):
		self.select_keys_x = express_chart_view.select_keys_x
		self.select_keys_y = express_chart_view.select_keys_y
		self.select_subgroup = express_chart_view.select_subgroup
		self.select_agg = express_chart_view.select_agg
		self.header = express_chart_view.header
		self.table_name = express_chart_view.table_name
		self.df = express_chart_view.df_to_revit
		self.key = key