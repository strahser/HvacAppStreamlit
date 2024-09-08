
import plotly.graph_objects as go

from library_hvac_app.list_custom_functions import to_list


class NetworkPlotlyPlotter:
	def __init__(self, network_list: list, df_network):
		self.network_list = to_list(network_list)
		self.df_network = df_network
		self.fig = go.Figure()
		"""
		fig_plotly = NetworkPlotlyPlotter(network_list=self.network_layout.networks_update,
		df_network=[network.df_branch for network in self.network_layout.networks_update])
		fig_plotly.add_location_point()
		st.plotly_chart(fig_plotly.fig)
		"""

	def get_intersection_column_name(self, df_network):
		"""choose column name from df (check vertical or horizontal orientation)"""
		if "y_cross_x" in df_network.columns:
			self.cross_x = "y_cross_x"
			self.cross_y = "y_cross_y"
		else:
			self.cross_x = "x_cross_x"
			self.cross_y = "x_cross_y"
	def add_location_point(self):
		marker = dict(
			size=12, line=dict(width=2, color='DarkSlateGrey'))
		for loc_point in self.network_list:
			loc_point_scatter = go.Scatter(
				x=[loc_point.system_location_point[0]],
				y=[loc_point.system_location_point[1]],
				mode="lines+markers+text",
				textposition="top center",
				name='location',
				marker=marker,
				text=loc_point.route_name
			)
			self.fig.add_trace(loc_point_scatter)

		for df_network in self.df_network:
			self.get_intersection_column_name(df_network)

			x_branch = df_network["pcx"]+df_network[self.cross_x]
			y_branch = df_network["pcy"]+df_network[self.cross_y]

			line = go.Line((df_network["pcx"],df_network["pcy"]),(df_network[self.cross_x],df_network[self.cross_y]),mode="markers+text")
			x_main = df_network[self.cross_x]
			y_main = df_network[self.cross_y]
			flow =  [f"L= {val}" for val in df_network['sum_column'].round()]
			m_idx = df_network['m_idx']
			main = go.Scatter(
				x=x_main,
				y=y_main,
				mode="lines+markers+text",
				marker=marker,
				textposition="bottom center",
				text=flow,
				name='main',
			)
			main_text = go.Scatter(
				x=x_main,
				y=y_main,
				mode="text",
				marker=marker,
				textposition="top center",
				text=m_idx,
				name='main',
			)
			self.fig.add_trace(line)
			self.fig.add_trace(main)
			self.fig.add_trace(main_text)

