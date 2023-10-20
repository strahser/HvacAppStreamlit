from dataclasses import dataclass, field, asdict
import streamlit as st


from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel


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
