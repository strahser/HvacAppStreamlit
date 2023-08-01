
from Networks.CalculationNetwork.NetworkBuilder import *
from Networks.NetworkLayouts.NetworkLayouts import *

class NetworkCreateSingleRoute:
    def __init__(
        self,
        df: pd.DataFrame,
        json_path: str,
        system_layouts:AddLayoutsToList,
        networks_layouts:list
        ) -> None:
        """mapping NetworkBuilder and layouts

        Args:
            df (pd.DataFrame): _description_
            json_path (str): _description_
        """
        self.df = df
        self.system_layouts = system_layouts
        self.networks_layouts = networks_layouts
        self.polygon_merge = PolygonMerge(
            self.df,
            json_path,
            self.system_layouts.system_choice,
            "S_level",
            self.system_layouts.level_val,
        )

    def __call__(self):
        self._creat_network_from_layoute_data()


    def get_network_builder_input_data(self)->list:
        """create list of dictionares of input for NetworkBuilder

        Returns:
            list: list of dict
        """
        builders_list = []
        for layout in self.networks_layouts:
            prefix_ = "_" + layout.system_number
            temp_dict = dict(
                polygon_merge= self.polygon_merge,
                system_location_point=(
                    getattr(layout, "local_point_x" + prefix_),
                    getattr(layout, "local_point_y" + prefix_),
                ),
                system_name=self.system_layouts.system_name_choice,
                sys_flow_column=self.system_layouts.sys_flow_choice,
                network_coordinate_x=(
                    getattr(layout, "network_start_point_x" + prefix_),
                    getattr(layout, "network_end_point_x" + prefix_),
                ),
                network_coordinate_y=(
                    getattr(layout, "network_start_point_y" + prefix_),
                    getattr(layout, "network_end_point_y" + prefix_),
                ),
                route_name=getattr(layout, "route_name" + prefix_),
            )
            builders_list.append(temp_dict)
        return builders_list


    def _creat_network_from_layoute_data(self):
        single_input_dict = self.get_network_builder_input_data()[0]

        self.network_builder = NetworkBuilder(
            polygon_merge = single_input_dict['polygon_merge'],
            system_location_point = single_input_dict['system_location_point'],
            system_name = single_input_dict['system_name'],
            sys_flow_column = single_input_dict['sys_flow_column'],
            network_coordinate_x = single_input_dict['network_coordinate_x'],
            network_coordinate_y = single_input_dict['network_coordinate_y'],
            route_name = single_input_dict['route_name'],
        )
        return self.network_builder

