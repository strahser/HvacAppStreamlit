import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from Networks.CalculationNetwork.PressureCalculator.GetLongRoute import GetLongRoute
from Networks.CalculationNetwork.StaticData.NetworkSessionConstants import GraphConstance, NetworkSessionConstants
from Networks.Utils.NetworkSession import get_session_system
from Polygons.PolygonPlot.PolygonPlotter import save_plot_to_svg


def visualise_graph(df: pd.DataFrame, system_name: str) -> None:
	system = get_session_system(system_name)
	# Create full  graph
	g = nx.from_pandas_edgelist(df, source=GraphConstance.from_branch, target=GraphConstance.to_branch,
	                            edge_attr=[GraphConstance.diameter, GraphConstance.flow, GraphConstance.full_pressure])
	# add plots
	fig, ax = plt.subplots(2, 1)
	ax[0].set_title(f'Main Scheme {system_name}')
	ax[1].set_title(f'Long Pressure Scheme {system_name}')
	# first plot create
	plt.subplot(2, 1, 1)
	plt.axis('off')
	plt.tight_layout()
	pos = nx.spring_layout(g, seed=5)
	edge_labels = dict(
		[((u, v,), f"d={d['diameter']}\nL={round(d['flow']):,}m3/h\nDP={round(d['full_pressure'])}Pa")
		 for u, v, d in g.edges(data=True)])
	options = {
		'arrowstyle': '-|>',
		'arrowsize': 12,
		"font_size": 12
	}
	nx.draw_networkx(g, pos=pos, with_labels=True, arrows=True, **options)
	nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8)
	# create long pressure graph
	ng = GetLongRoute(df, 'from_branch', 'to_branch', "full_pressure")
	try:
		long_path = ng.get_long_df()
		plt.subplot(2, 1, 2)
		plt.axis('off')
		plt.tight_layout()
		edge_labels2 = dict([((u, v,), f"DP={round(d['full_pressure'])}Pa")
		                     for u, v, d in g.edges(data=True)])
		g2 = nx.from_pandas_edgelist(long_path, source='from_branch', target='to_branch',
		                             edge_attr=["full_pressure"])
		nx.draw_networkx(g2, pos=pos, with_labels=True, arrows=True, **options)
		nx.draw_networkx_edge_labels(g2, pos, edge_labels=edge_labels2, font_size=8)
		pressure_value = str(round(long_path['full_pressure'].sum()))
		flow_value = round(df['flow'].max())
		system[NetworkSessionConstants.calculated_pressure] = pressure_value
		system[NetworkSessionConstants.calculated_flow] = flow_value
	except Exception as e:
		st.warning(e)
	fig.set_size_inches(10, 10)
	system[NetworkSessionConstants.graph_plot] = save_plot_to_svg(fig)
