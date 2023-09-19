import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from AnalyticalTables.AnalyticalControls.GroupTableControl import *
from AnalyticalTables.AnalyticalControls.PivotTableControl import *
from SQL.SqlControl.SqlQueryViewTableControl import *


class PivotAndGroupTableControl():
	def __init__(self):
		self.pivot_table = None
		self.group_table = None

	def create_pivot_and_group_table(self, df: pd.DataFrame, show_input_df: bool = True):

		if show_input_df:
			st.expander("Show Table").write(df)
		with st.expander("Group Table"):
			col1, col2, col3 = st.columns([2, 4, 6])
			with col1:
				self.group_table = GroupTableControl(df)
			with col2:
				self.group_table.show_group_table()
			with col3:
				st.subheader("Main Charts")
				self._create_charts()

		with st.expander("Pivot Table"):
			col1, col2 = st.columns([2, 10])
			with col1:
				self.pivot_table = PivotTableControl(df)
			with col2:
				self.pivot_table.show_pivot_table()

	def _create_charts(self):
		try:
			df = self.group_table.get_group_table()
			fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
			st.subheader("Bar chart")
			st.bar_chart(df,
			             x=self.group_table.group_table_view.group_field,
			             y=self.group_table.group_table_view.agg_field)
			st.subheader("Area chart")
			st.area_chart(df,
			              x=self.group_table.group_table_view.group_field,
			              y=self.group_table.group_table_view.agg_field)
			labels = df[self.group_table.group_table_view.group_field]
			values = df[self.group_table.group_table_view.agg_field[0]]
			st.subheader("Percent")
			fig.add_trace(go.Pie(labels=labels,
			                     values=values, textinfo='label+percent',
			                     insidetextorientation='radial'), 1, 1)

			st.plotly_chart(fig)

		except Exception as e:
			st.warning(e)
