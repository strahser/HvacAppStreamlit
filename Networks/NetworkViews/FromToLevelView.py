from Networks.CalculationNetwork.StaticData.NetworkSessionConstants import GraphConstance, NetworkSessionConstants
from Networks.PloteNetwork.PlotDataFromSession import get_session_system

import streamlit as st


class FromToLevelView:
	def __init__(self, level_list: list[str], system_name, key: str):
		self.system_name = system_name
		self.key = key
		self.columns = st.columns(4)
		self.level_list = level_list

	def create_table(self):
		self.__create_table_header()
		number_columns = st.columns(6)
		with number_columns[5]:
			self.level_chain_quantity = st.number_input(
				"select level chain quantity",
				value=len(self.level_list),
				step=1,
				key=f"level_chain_quantity {self.key}"
			)
			self.add_table_to_session = st.button("Confirm", key=f"add_table_to_session button {self.key}")
			system = get_session_system(self.system_name)
			dict_to_df = {
				GraphConstance.system_type: None,
				GraphConstance.from_branch: self.__create_table_from_to(0, GraphConstance.from_branch).values(),
				GraphConstance.to_branch: self.__create_table_from_to(1, GraphConstance.to_branch).values(),
				GraphConstance.distance: self.__add_distance_column(2).values(),
				GraphConstance.flow: self.__add_flow_column(3).values(),
			}
			system[NetworkSessionConstants.df_from_to_level] = dict_to_df

	def __create_table_header(self)->None:
		data_list = [GraphConstance.from_branch, GraphConstance.to_branch, GraphConstance.distance, GraphConstance.flow]
		for en, data in enumerate(data_list):
			self.columns[en].write(data)

	def __add_distance_column(self, index_columns: int):
		res = {}
		for i in range(self.level_chain_quantity):
			distance = self.columns[index_columns].number_input("distance", key=f"distance_column_value{i} {self.key}",
			                                                    label_visibility="collapsed", value=10)

			res[f"distance_column_value{i} {self.key}"] = distance
		return res

	def __add_flow_column(self, index_columns: int):
		res = {}
		for i in range(self.level_chain_quantity):
			flow = self.columns[index_columns].number_input("flow", key=f"flow_column_value{i} {self.key}",
			                                                label_visibility="collapsed")
			res[f"flow_column_value{i}"] = flow

		return res

	def __create_table_from_to(self, index_columns: int, key_label: str = "from"):
		res = {}
		for i in range(self.level_chain_quantity):
			select_columns = self.columns[index_columns].selectbox("select data from",
			                                                       self.level_list,
			                                                       key=f"{key_label}{i}  {self.key}",
			                                                       label_visibility="collapsed")
			res[f"{key_label}{i}  {self.key}"] = select_columns
		return res
