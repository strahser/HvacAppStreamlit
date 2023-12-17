import streamlit as st
from Session.StatementConfig import StatementConstants


class NetworkSessionConstants:
	system_type = "system_type"
	full_pressure_df = "full pressure df"
	calculated_pressure = "calculated pressure"
	calculated_flow = "calculated flow"
	graph_plot = "graph plot"
	df_from_to_level = "df_from_to_level"
	temp_fig_data = "temp_fig_data"
	excluding_list = [system_type, full_pressure_df, calculated_pressure, calculated_flow, graph_plot, df_from_to_level,
	                  temp_fig_data]





class GraphConstance:
	from_branch = 'from_branch'
	to_branch = "to_branch"
	diameter = "diameter"
	distance = "distance"
	flow = "flow"
	full_pressure = "full_pressure"
	system_type = "system_type"
