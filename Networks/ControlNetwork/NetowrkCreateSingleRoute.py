from Networks.CalculationNetwork.NetworkBuilder import NetworkBuilder
from Networks.NetworkViews.NetworkMainView import NetworkMainView, NetworkConfigView
from Networks.plote_polygons.PolygonMerge import PolygonMerge
import pandas as pd


class NetworkCreateSingleRoute:
	def __init__(
			self,
			df: pd.DataFrame,
			json_path: str,
			network_main_view: NetworkMainView,
			network_config_view: NetworkConfigView,
			networks_layouts: list,
			level_location_point_coordinates
	):
		"""mapping NetworkBuilder and layouts

        Args:
            df (pd.DataFrame): _description_
            json_path (str): _description_
        """
		self.df = df
		self.network_main_view = network_main_view
		self.polygon_merge = PolygonMerge(
			self.df,
			json_path,
			network_main_view.network_system_view.system_choice,
			network_main_view.network_system_view.level_column,
			network_config_view.network_level_view.level_val,
		)
		self.system_layouts = network_main_view
		self.level_location_point_coordinates = level_location_point_coordinates
		self.networks_layouts = networks_layouts

	def __call__(self):
		self._create_network_from_layout_data()

	def get_network_builder_input_data(self) -> list[dict]:
		"""create list of dictionares of input for NetworkBuilder

        Returns:
            list: list of dict
        """
		builders_list = []
		for layout in self.networks_layouts:
			prefix_ = "_" + str(layout.system_number)
			temp_dict = dict(
				polygon_merge=self.polygon_merge,
				system_location_point=self.level_location_point_coordinates,
				system_name=self.network_main_view.network_system_view.system_name_choice,
				sys_flow_column=self.network_main_view.network_system_view.sys_flow_choice,
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

	def _create_network_from_layout_data(self):
		single_input_dict = self.get_network_builder_input_data()[0]
		self.network_builder = NetworkBuilder(
			polygon_merge=single_input_dict['polygon_merge'],
			system_location_point=single_input_dict['system_location_point'],
			system_name=single_input_dict['system_name'],
			sys_flow_column=single_input_dict['sys_flow_column'],
			network_coordinate_x=single_input_dict['network_coordinate_x'],
			network_coordinate_y=single_input_dict['network_coordinate_y'],
			route_name=single_input_dict['route_name'],
		)
		return self.network_builder
