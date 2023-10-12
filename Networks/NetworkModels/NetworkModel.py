from dataclasses import dataclass, field
import pandas as pd
import streamlit as st
import datetime


@dataclass
class NetworkBranchModel:
	system_name: str
	system_type: str
	system_level: str
	network_draft_plot_data: str
	network_pressure_plot_data: str
	network_long_plot_data: str
	network_pressure_table: pd.DataFrame
	network_long_pressure_table: pd.DataFrame
	network_draft_plot_name: str = "Draft plot"
	network_pressure_plot_name: str = "Pressure plot"
	network_long_plot_name: str = "Long Pressure plot"
	network_table_pressure_name: str = "Pressure drop calculation"
	network_table_main_route_pressure_name: str = "Main route Pressure drop calculation"
	branch_name: str = field(init=False)
	data_create: str = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}'

	def __post_init__(self):
		self.branch_name = f"{self.system_name}_{self.system_level}"


@dataclass
class NetworkSystemModel:
	system_name: str
	system_type: str
	network_branch_list: [NetworkBranchModel] = field(default_factory=list)

	def add_branches(self, branch_instance: NetworkBranchModel) -> None:
		branch_list = [val.branch_name for val in self.network_branch_list]
		st.write(f"{self.system_name}_{branch_instance.system_level}" in branch_list)
		st.write(f"{self.system_name}_{branch_instance.system_level}" == branch_instance.branch_name)
		if f"{self.system_name}_{branch_instance.system_level}" in branch_list:
			for en, val in enumerate(self.network_branch_list):
				if f"{self.system_name}_{branch_instance.system_level}" == branch_instance.branch_name:
					self.network_branch_list[en] = branch_instance
		else:
			self.network_branch_list.append(branch_instance)

	def create_branch_name(self) -> None:
		for branch in self.network_branch_list:
			branch.create_branch_name(self.system_name)


if __name__ == "__main__":
	n_branch = NetworkBranchModel("level", "drat plot", "pressure plot", "long_plot", )
	n_branch1 = NetworkBranchModel("level1", "drat plot", "pressure plot", "long_plot", )
	system = NetworkSystemModel("S1", "ventilation")
	system.add_branches(n_branch)
	system.add_branches(n_branch1)
	system.create_branch_name()
	print(system)
