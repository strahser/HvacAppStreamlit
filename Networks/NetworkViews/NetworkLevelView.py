import streamlit as st


class NetworkLevelView:
	def __init__(self, level_list: list[str], level_index, key):
		branches_table_columns = st.columns(3)
		self.local_point_x: float = branches_table_columns[0].number_input("input location point x", value=20000,
		                                                                   key=f"{key} local_point_x")
		self.local_point_y = branches_table_columns[1].number_input("input location point y", value=0,
		                                                            key=f"{key} local_point_y")
		self.level_val = st.selectbox("choose level", level_list, index=level_index, key=f"{key} level_val")
		self.system_number = st.number_input("choose number of system", min_value=1, value=1,
		                                     key=f"{key} system_number")