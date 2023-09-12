import json

from Networks.CalculationNetwork.NetworkEngineer import ExcelLoader
from Networks.CalculationNetwork.NetworkMultyCreation import NetworkMultyCreate
from Networks.ControlNetwork.NetowrkCreateSingleRoute import *
from Networks.CalculationNetwork.NetworkAddPressureToDF import *


class CreateMainNetworkLayout:
    def __init__(
        self,
        df_to_revit: pd.DataFrame,
        json_path: json,
        input_settings_df: pd.DataFrame,
    ) -> list:
        """populate layout and network

        Args:
            df_to_revit (pd.DataFrame): _description_
            json_path (json): _description_
            input_settings_df (pd.DataFrame): _description_
            df_to_revit_path = path_init(myDir, "inputData", "to_revit.xlsx")
            setting_path = path_init(myDir, "inputData", "settings.xlsx")
            json_path = path_init(myDir, "inputData", "polygon_data_file.json")
            df_to_revit = pd.read_excel(df_to_revit_path)
            medium_property = pd.read_excel(setting_path, None)
        """
        self.df_to_revit = df_to_revit
        self.json_path = json_path
        self.input_settings_df = input_settings_df

    def create_main_layout(self):
        self.layout = AddLayoutsToList(self.df_to_revit, self.input_settings_df)
        self.system_layouts = self.layout.create_system_layout()
        self.network_layout = self.layout.create_network_layout()
        self.layout.create_from_to_layout()

    def checking_from_to_list_layout(self):
        if (
            self.layout.columns_number == 2
            and self.layout.network_from_1
            and self.layout.network_from_1 != self.layout.network_to_1
        ):
            return [(self.layout.network_from_1, self.layout.network_to_1)]
        elif self.layout.columns_number == 3:  # option
            return [
                (self.layout.network_from_1, self.layout.network_to_1),
                (self.layout.network_from_2, self.layout.network_to_2),
            ]
        else:
            return []

    def get_from_to_layout_data(self):
        self.list_of_from_to = self.checking_from_to_list_layout()
        self.list_of_from = [sublist[0] for sublist in self.list_of_from_to]

    def add_layout_data_to_network_calculation(self):
        network = NetworkCreateSingleRoute(
            self.df_to_revit, self.json_path, self.system_layouts, self.network_layout
        )
        network_builder_list_data = network.get_network_builder_input_data()
        self.networks_update = NetworkMultyCreate.add_networks(
            network_builder_list_data, self.list_of_from_to
        )
        
        return self.networks_update

    def add_layout_data_to_pressure_calculation(self)->NetworkAddPressure:
        self.add_layout_data_to_network_calculation()
        excel_loader = ExcelLoader(
            self.system_layouts.system_type_choice, self.input_settings_df
        )
        self.pressuer_df_list = []
        for network in self.networks_update:
            pressuer_df = NetworkAddPressure(
                excel_loader, network, network.df_branch, self.list_of_from
            )
            self.pressuer_df_list.append(pressuer_df)
        return self.pressuer_df_list

    def __call__(self) -> list:
        self.create_main_layout()
        self.get_from_to_layout_data()
        self.add_layout_data_to_network_calculation()
        return self.add_layout_data_to_pressure_calculation()
