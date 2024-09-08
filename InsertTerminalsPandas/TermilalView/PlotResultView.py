import streamlit as st


class PlotResultLayout:
	def __init__(self, save_fig: str, df_result_list: list, system_list: list, level_label: str = None) -> None:
		self.save_fig = save_fig
		self.df_result_list = df_result_list
		self.system_list = system_list
		self.level_label = level_label

	def create_plot_results_layout(self):
		st.subheader(f"Level {self.level_label}")
		with st.expander(":heavy_plus_sign:"):
			st.write(self.save_fig, unsafe_allow_html=True)

	def create_data_frame_results_layout(self):
		st.subheader(f"Level {self.level_label}")
		with st.expander(":heavy_plus_sign:"):
			for df_res, sys_name in zip(self.df_result_list, self.system_list):
				st.subheader(f'{sys_name.title().replace("_", " ")} result')
				st.dataframe(df_res)