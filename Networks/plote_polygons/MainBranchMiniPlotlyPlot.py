from Networks.NetworkViews.NetworkBranchesView import NetworkBranchesView
from Networks.NetworkViews.NetworkConfigView import NetworkConfigView
from Session.StatementConfig import StatementConstants
import plotly.graph_objects as go
import streamlit as st
from dataclasses import dataclass


@dataclass
class NetworkMiniPlotModelData:
	level_value: str
	system_name_choice: str
	networks_layouts_list: list[NetworkBranchesView]
	level_location_point_coordinates: tuple[float, float]


class MainBranchMiniPlotlyPlot:
	def __init__(self, network_config_view: NetworkConfigView, fig: go.Figure,level_flow_data:float):
		self.network_config_view = network_config_view
		self.level_flow_data =level_flow_data
		self.fig = fig if fig else None

	def create_mini_plots(self) -> go.Figure:
		try:
			level_value = self.network_config_view.level_value
			if self.fig:
				x_center, y_center = self.network_config_view.level_location_point_coordinates
				point = go.Scatter(
					x=(x_center,),
					y=(y_center,),
					textfont=dict(size=18, family="Issocuper", color="black"),
					text=f"<em>{self.network_config_view.system_name_choice},Q={self.level_flow_data}</em>",
					textposition='top center',
					name=f"<em>{level_value}, {self.network_config_view.system_name_choice}, Q={self.level_flow_data}</em>",
					marker=dict(size=20, line=dict(width=2, color='DarkSlateGrey')),
					mode="markers+lines+text")
				self.fig.add_trace(point)
				for network in self.network_config_view.network_branches_view_list:
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
					self.fig.add_trace(line)
				self.fig.update_xaxes(
					showgrid=True,
					zeroline=True,
					showticklabels=True
				)
				self.fig.update_yaxes(
					showgrid=True,
					zeroline=True,
					showticklabels=True
				)
				return self.fig
		except Exception as e:
			st.warning(e)
