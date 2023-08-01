from DashBoard.ExpressCharts import StreamlitExpressChartsView
from DashBoard.ExpressCharts._TableControl import _TableControl
from library_hvac_app.html.Layouts import make_grid
import plotly.express as px
import streamlit as st


class StreamlitExpressCharts(_TableControl):
	def __init__(self, express_chart_view: StreamlitExpressChartsView, key, agg_func: str):
		super().__init__(express_chart_view, key)
		self.agg_func = agg_func
		self.key = key

	def create_plotly_dynamic_charts(self):
		self.agg_df = self.df.groupby(self.select_keys_x, as_index=False)[self.select_keys_y].agg(self.agg_func)
		st.markdown(f"#### {self.agg_func.title()} Group Data Table")
		st.write(self.agg_df)
		grid = make_grid(2, 2)
		bar = px.bar(self.agg_df, x=self.select_keys_x, y=self.select_keys_y, title=f"{self.agg_func.title()} Bar")
		scatter = px.scatter(self.df, x=self.select_keys_x, y=self.select_keys_y,
		                     title=f"{self.agg_func.title()}Scatter")
		hist = px.histogram(self.df, x=self.select_keys_y, title=f"{self.agg_func.title()} Histogram")
		pie = px.pie(self.agg_df, names=self.select_keys_x, values=self.select_keys_y,
		             title=f"{self.agg_func.title()} Pie")
		all_charts = ((bar, scatter), (hist, pie))
		for en_row, row in enumerate(all_charts):
			for en_col, col in enumerate(row):
				with grid[en_row][en_col]:
					st.plotly_chart(col)