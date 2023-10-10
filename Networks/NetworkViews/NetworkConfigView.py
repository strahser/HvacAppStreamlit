import pandas as pd
import streamlit as st
from Networks.NetworkViews.NetworkBranchesView import NetworkBranchesView
from Networks.NetworkViews.NetworkLevelView import NetworkLevelView
from Networks.NetworkViews.NetworkSystemView import NetworkSystemView
from Networks.plote_polygons.MainBranchPlotlyPlot import MainBranchPlotlyPlot


class NetworkConfigView:
	def __init__(self, df: pd.DataFrame, network_system_view: NetworkSystemView):
		self.df = df
		self.network_system_view = network_system_view
		self.from_to_list = None
		self.networks_layouts_list = None
		self.branch_number = None
		self.level_location_point_coordinates = None
		self.network_level_view = None

	def create_network_layout(self, level_list: list[str], level_index: int):
		st.subheader("Level Location point")
		self.network_level_view = NetworkLevelView(level_list, level_index,
		                                           key=f"LevelLocationPoint {level_list[level_index]}")
		self.level_location_point_coordinates = (
			self.network_level_view.local_point_x, self.network_level_view.local_point_y)
		self.branch_number = self.network_level_view.system_number
		self.networks_layouts_list = []
		self.__create_table_title()
		for i in range(self.branch_number):
			temp = NetworkBranchesView(self.df, self.network_level_view.level_val, i + 1, self.branches_table_columns)
			self.networks_layouts_list.append(temp)
		return self.networks_layouts_list

	def __create_table_title(self) -> st.columns:
		st.subheader("Network Coordinates")
		table_header = ["Network Name", "start x", "end x", "start y", "end y", "system prefix"]
		self.branches_table_columns = st.columns(len(table_header))
		for en, val in enumerate(table_header):
			self.branches_table_columns[en].write(val)

	def create_BranchPlotlyPlot(self):
		fig = MainBranchPlotlyPlot.create_branch_plots(self)
		if fig:
			st.plotly_chart(fig)

	def create_from_to_layout(self):
		st.subheader(f"from to connection")
		options = [
			getattr(temp, "route_name" + "_" + str(en + 1))
			for en, temp in enumerate(self.networks_layouts_list)
		]
		columns = st.columns(6)
		self.from_to_list = []
		columns[0].write("From")
		columns[1].write("To")
		for i in range(self.branch_number - 1):
			if self.network_level_view.system_number >= 2:
				network_from_to_dict = dict(
					network_from=columns[0].selectbox(
						label=f"select from",
						options=options,
						key=f"network_from {self.network_system_view.system_name_choice} {self.network_level_view.level_val} {i}",
						label_visibility="collapsed"),
					network_to=columns[1].selectbox(
						label=f"select to",
						options=options,
						key=f"network_to {self.network_system_view.system_name_choice} {self.network_level_view.level_val} {i}",
						label_visibility="collapsed")
				)
				temp_list = []
				for key, val in network_from_to_dict.items():
					setattr(self, f"{key}_{i + 1}", val)
					temp_list.append(getattr(self, f"{key}_{i + 1}"))
				self.from_to_list.append(temp_list)
