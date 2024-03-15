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
			col1, col2 = st.columns([2,6])
			with col1:
				self.group_table = GroupTableControl(df)
			with col2:
				self.group_table.show_group_table()

			st.subheader("Main Charts")
			self._create_charts()

		with st.expander("Pivot Table"):
			col1, col2 = st.columns([2, 10])
			with col1:
				self.pivot_table = PivotTableControl(df)
			with col2:
				self.pivot_table.show_pivot_table()

	def _create_charts(self):
		col1, col2,col3 = st.columns(3)
		try:
			df = self.group_table.get_group_table()
			x_data = self.group_table.group_table_view.group_field
			ydata = self.group_table.group_table_view.agg_field
			for en, data in enumerate(x_data):
				fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
				with col1:
					st.subheader("Bar chart")
					st.bar_chart(df,
					             x=x_data[en],
					             y=ydata)
				with col2:
					st.subheader("Area chart")
					st.area_chart(df,
					              x=x_data[en],
					              y=ydata)
				with col3:
					labels = df[x_data[en]]
					values = df[ydata[en]]
					st.subheader("Percent")
					fig.add_trace(go.Pie(labels=labels,
					                     values=values, textinfo='label+percent+value',
					                     insidetextorientation='radial',
					                     ), 1, 1
					              )
					fig.update_layout(legend={'traceorder': 'normal'})
					st.plotly_chart(fig)

		except Exception as e:
			st.warning(e)
