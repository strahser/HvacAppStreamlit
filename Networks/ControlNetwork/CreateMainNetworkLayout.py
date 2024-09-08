from Networks.CalculationNetwork.NetworkEngineer import ExcelQuery
from Networks.CalculationNetwork.NetworkMultyCreation import NetworkMultyCreate
from Networks.CalculationNetwork.PressureCalculator.NetworkAddPressure import NetworkAddPressure
from Networks.ControlNetwork.NetowrkCreateSingleRoute import *
from Networks.NetworkViews.NetworkMainView import NetworkConfigView


class CreateMainNetworkLayout:
	def __init__(self, network_main_view: NetworkMainView, network_config_view: NetworkConfigView, json_path: str):
		self.network_main_view = network_main_view
		self.df_to_revit = network_main_view.df_to_revit
		self.input_settings_df = network_main_view.input_settings_df
		self.network_config_view = network_config_view
		self.json_path = json_path
		self.pressure_df_list = None
		self.networks_update = None
		self.list_of_from = None
		self.list_of_from_to = None
		self.network_layout_list = None

	def create_main_layout(self):
		self.network_layout_list = self.network_config_view.network_branches_view_list

	def get_from_to_layout_data(self):
		self.list_of_from_to = self.network_config_view.from_to_list
		self.list_of_from = [sublist[0] for sublist in self.list_of_from_to]

	def add_layout_data_to_network_calculation(self):
		network = NetworkCreateSingleRoute(
			self.df_to_revit,
			self.json_path,
			self.network_main_view,
			self.network_config_view,
			self.network_layout_list,
			self.network_config_view.level_location_point_coordinates
		)
		network_builder_list_data = network.get_network_builder_input_data()
		self.networks_update = NetworkMultyCreate.add_networks(network_builder_list_data, self.list_of_from_to)
		return self.networks_update

	def add_layout_data_to_pressure_calculation(self) -> list[NetworkAddPressure]:
		self.add_layout_data_to_network_calculation()
		excel_loader = ExcelQuery(self.network_main_view.system_type_choice, self.input_settings_df)
		self.pressure_df_list = []
		for network in self.networks_update:
			presser_df = NetworkAddPressure(excel_loader, network, network.df_branch, self.list_of_from)
			self.pressure_df_list.append(presser_df)
		return self.pressure_df_list

	def __call__(self) -> list:
		self.get_from_to_layout_data()
		self.add_layout_data_to_network_calculation()
		return self.add_layout_data_to_pressure_calculation()
