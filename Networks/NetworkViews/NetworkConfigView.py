import pandas as pd
import streamlit as st
from Networks.NetworkViews.NetworkBranchesView import NetworkBranchesView


class NetworkConfigView:
	def __init__(self, df: pd.DataFrame, system_name_choice: str, key: str):
		self.key = key
		self.df = df
		self.system_name_choice = system_name_choice
		self.from_to_list = None
		self.network_branches_view_list = None
		self.branch_number = None
		self.level_location_point_coordinates = None

	def create_network_layout(self, level_list: list[str], level_index: int):
		st.subheader("Level Location point")
		key = f"LevelLocationPoint {level_list[level_index]}"
		branches_table_columns = st.columns(3)
		self.local_point_x: float = branches_table_columns[0].number_input("input location point x", value=20000,
		                                                                   key=f"{key} local_point_x {self.key}")
		self.local_point_y: float = branches_table_columns[1].number_input("input location point y", value=0,
		                                                                   key=f"{key} local_point_y {self.key}")
		self.level_value: str = st.selectbox("choose level", level_list, index=level_index,
		                                     key=f"{key} level_val {self.key}")
		self.system_number: int = st.number_input("choose number of system", min_value=1, value=1,
		                                          key=f"{key} system_number {self.key}")

		self.level_location_point_coordinates = (
			self.local_point_x, self.local_point_y)
		self.branch_number = self.system_number
		self.network_branches_view_list = []
		self.__create_table_title()
		for i in range(self.branch_number):
			temp = NetworkBranchesView(self.df, self.level_value, i + 1, self.branches_table_columns, self.key)
			self.network_branches_view_list.append(temp)
		return self.network_branches_view_list

	def __create_table_title(self) -> st.columns:
		st.subheader("Network Coordinates")
		table_header = ["Network Name", "start x", "end x", "start y", "end y", "system prefix"]
		self.branches_table_columns = st.columns(len(table_header))
		for en, val in enumerate(table_header):
			self.branches_table_columns[en].write(val)

	def create_from_to_layout(self):
		st.subheader(f"from to connection")
		options = [
			getattr(temp, "route_name" + "_" + str(en + 1))
			for en, temp in enumerate(self.network_branches_view_list)
		]
		columns = st.columns(6)
		self.from_to_list = []
		columns[0].write("From")
		columns[1].write("To")
		for i in range(self.branch_number - 1):
			if self.system_number >= 2:
				network_from_to_dict = dict(
					network_from=columns[0].selectbox(
						label=f"select from",
						options=options,
						key=f"network_from {self.system_name_choice} {self.level_value} {i}  {self.key}",
						label_visibility="collapsed"),
					network_to=columns[1].selectbox(
						label=f"select to",
						options=options,
						key=f"network_to {self.system_name_choice} {self.level_value} {i}  {self.key}",
						label_visibility="collapsed")
				)
				temp_list = []
				for key, val in network_from_to_dict.items():
					setattr(self, f"{key}_{i + 1} {self.key}", val)
					temp_list.append(getattr(self, f"{key}_{i + 1} {self.key}"))
				self.from_to_list.append(temp_list)
