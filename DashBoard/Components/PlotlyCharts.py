from Upload.Session.StatementConfig import StatementConstants
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

def load_plotly_charts(selected_levels:list[str],is_need_show_plots:bool,level_plots_data:dict[str:dict]|None):
	if is_need_show_plots:
		plt_list = []
		plt_levels =[]
		if level_plots_data:
			for level in selected_levels:
				f_html = level_plots_data[level]
				fig = go.Figure(data=f_html['data'], layout=f_html['layout'])
				plt_image = pio.to_image(fig, "svg")#optional
				plt_list.append(fig)
				plt_levels.append(level)
			return plt_list,plt_levels