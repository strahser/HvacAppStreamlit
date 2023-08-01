import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
# from dtale.app import get_instance
# from dtale.views import startup
from AnalyticalTables.AnalyticalControls.GroupTableControl import *
from AnalyticalTables.AnalyticalControls.PivotTableControl import *
from SQL.SqlControl.SqlQueryViewTableControl import *


class PivotAndGroupTableControl():
	def __init__(self):
		self.pivot_table = None
		self.group_table = None
		self.input_tab, self.data_tab = st.tabs(["Input data", "Result data"])

	def create_pivot_and_group_table(self, df: pd.DataFrame):
		with st.container():  # group tables and charts
			with self.input_tab:
				st.expander("Show Table").write(df)
				self.group_table = GroupTableControl(df)
				self.pivot_table = PivotTableControl(df)
			with self.data_tab:
				col1, col2 = st.columns(2)
				with col1:
					self.group_table.show_group_table()
					self.pivot_table.show_pivot_table()
				with col2:
					st.subheader("Main Charts")
					self._create_charts()

	def _create_charts(self):
		try:
			fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
			st.subheader("Bar chart")
			st.bar_chart(self.group_table.get_group_table(),
			             x=self.group_table.group_table_view.group_field,
			             y=self.group_table.group_table_view.agg_field)
			st.subheader("Area chart")
			st.area_chart(self.group_table.get_group_table(),
			              x=self.group_table.group_table_view.group_field,
			              y=self.group_table.group_table_view.agg_field)
			labels = self.group_table.get_group_table()[self.group_table.group_table_view.group_field].to_list()
			values = self.group_table.get_group_table()[self.group_table.group_table_view.agg_field[0]].to_list()
			st.subheader("Percent")
			fig.add_trace(go.Pie(labels=labels,
			                     values=values, textinfo='label+percent',
			                     insidetextorientation='radial'), 1, 1)

			st.plotly_chart(fig)

		except:
			st.warning("Check data for group table plotting")

	def show_pivot_and_group_table(self):
		col = st.columns([4, 2])
		with col[1]:
			self.pivot_table.show_pivot_table()
		with col[1]:
			self.group_table.show_group_table()
