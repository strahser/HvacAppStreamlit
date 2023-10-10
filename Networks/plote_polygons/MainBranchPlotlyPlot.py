from Session.StatementConfig import StatementConstants
import plotly.graph_objects as go
import streamlit as st


class MainBranchPlotlyPlot:
	@staticmethod
	def create_branch_plots(layout) -> go.Figure:
		try:
			level_value = layout.network_level_view.level_val
			f_html = st.session_state[StatementConstants.levels_plots][level_value]
			fig = go.Figure(data=f_html['data'], layout=f_html['layout'])
			x_center, y_center = layout.level_location_point_coordinates
			point = go.Scatter(
				x=(x_center,),
				y=(y_center,),
				text=layout.network_system_view.system_name_choice,
				name=f"{level_value} {layout.network_system_view.system_name_choice}",
				marker=dict(size=20,
				            line=dict(width=2,
				                      color='DarkSlateGrey')
				            ),
				mode="markers+lines+text",
			)
			fig.add_trace(point)
			for network in layout.networks_layouts_list:
				x = (
					getattr(network, f"network_start_point_x_{network.system_number}"),
					getattr(network, f"network_end_point_x_{network.system_number}")
				)
				y = (
					getattr(network, f"network_start_point_y_{network.system_number}"),
					getattr(network, f"network_end_point_y_{network.system_number}")
				)
				branch_name = getattr(network, f"route_name_{network.system_number}")
				line = go.Scatter(mode="markers+lines+text",
				                  x=x,
				                  y=y,
				                  line=dict(width=6),
				                  text=branch_name,
				                  name=branch_name
				                  )
				fig.add_trace(line)
			fig.update_xaxes(
				showgrid=True,
				zeroline=True,
				showticklabels=True
			)
			fig.update_yaxes(
				showgrid=True,
				zeroline=True,
				showticklabels=True
			)
			return fig
		except Exception as e:
			st.warning(e)
