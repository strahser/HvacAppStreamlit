import streamlit as st
import pandas as pd


class NetworkBranchesView:
	def __init__(self, df: pd.DataFrame, level: str, system_number: int, branches_table_columns: st.columns, key: str):
		self.key = key
		self.system_number = system_number
		self.df = df
		self.level = level
		self.branches_table_columns = branches_table_columns
		self._network_name()
		self._start_and_end_network_points()
		self._prefix_name()

	def _network_name(self):
		with self.branches_table_columns[0]:
			st.text_input("network name", value=f"Network # {self.system_number}", label_visibility="collapsed",
			              key=f"network name {self.level} {self.system_number} {self.key}")

	def _start_and_end_network_points(self):
		with self.branches_table_columns[1]:
			start_point_x = st.number_input("network start point x", value=-25000, label_visibility="collapsed",
			                                key=f"start_point_x {self.level} {self.system_number} {self.key}")
		with self.branches_table_columns[2]:
			end_point_x = st.number_input("network end point x", value=20000, label_visibility="collapsed",
			                              key=f"end_point_x {self.level} {self.system_number} {self.key}")
		with self.branches_table_columns[3]:
			start_point_y = st.number_input("network start point y", value=0, label_visibility="collapsed",
			                                key=f"start_point_y {self.level} {self.system_number} {self.key}")
		with self.branches_table_columns[4]:
			end_point_y = st.number_input("network end point y", value=0, label_visibility="collapsed",
			                              key=f"end_point_y {self.level} {self.system_number} {self.key}")
		network_point_dict = dict(
			network_start_point_x=start_point_x,
			network_end_point_x=end_point_x,
			network_start_point_y=start_point_y,
			network_end_point_y=end_point_y,
		)
		for key, val in network_point_dict.items():
			setattr(self, key + "_" + str(self.system_number), val)

	def _prefix_name(self):
		with self.branches_table_columns[5]:
			route_name = st.text_input("choose system prefix", value=f"{self.system_number}",
			                           label_visibility="collapsed",
			                           key=f"route_name {self.level} {self.system_number}  {self.key}")
			prefix_dict = dict(
				route_name=route_name)
			for key, val in prefix_dict.items():
				setattr(self, key + "_" + str(self.system_number), val)
