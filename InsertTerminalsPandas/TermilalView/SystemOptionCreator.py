import pandas as pd
import streamlit as st

from InsertTerminalsPandas.TermilalView.ConfigStaticView import SystemPropertyModel


class SystemOptionCreator:
	"""do not in use. For changing excel system select sheet"""
	def __init__(self, selected_df: pd.DataFrame):
		self.system_dictionary = {}
		self.key = 0
		self.selected_df = selected_df
		st.write("Create System")
		self.choose_system_number = st.number_input("Select System number", min_value=1, value=3)

	def create_system_options(self):
		col1, col2, col3 = st.columns(3)
		col1.write("System Type Name")
		col2.write("System Flow Column")
		col3.write("System Name Column")
		input_data_list = []
		select_flow_list = []
		select_system_list = []
		for val in range(self.choose_system_number):
			input_data = col1.text_input("system", value="supply_system", label_visibility="hidden",
			                             key=f"input{val}")
			select_flow = col2.selectbox("system", self.selected_df.columns, label_visibility="hidden",
			                             key=f"flow system{val}")
			select_system = col3.selectbox("system", self.selected_df.columns, label_visibility="hidden",
			                               key=f"system name{val}")
			if input_data not in input_data_list:
				self.system_dictionary.update(
					{input_data: SystemPropertyModel(system_flow=select_flow, system_name=select_system)}
				)
				input_data_list.append(input_data)
				select_flow_list.append(select_flow)
				select_system_list.append(select_system)
			else:
				st.warning(f"ERROR multi name {input_data}")