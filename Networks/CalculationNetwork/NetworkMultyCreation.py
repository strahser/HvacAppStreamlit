import pandas as pd
from itertools import combinations
import collections

from Networks.CalculationNetwork.NetworkBuilder import NetworkBuilder


class NetworkMultyCreate:
    """ create_network_builder_list. product_networks and again create_network_builder_list

    Returns:
        _type_: _description_
    """

    @staticmethod
    def add_networks(network_builder_list_data:list[dict], add_row_list: list)->list:
        """create chain of instance of network_builder_list_

        Args:
            network_builder_list_data (list): network_builder_list_data = [input_list1, input_list2, input_list3]
            add_row_list (list): list_of_from_to = [["m_3", "m_1"], ["m_2", "m_1"]]
            sample

        Returns:
            _type_: _description_
        """
        def create_chain_of_update():
            network_add_route = NetworkProduct(network_builder_list_data)
            networks = network_add_route.create_network_builder_list()
            network_product_result = network_add_route.product_networks(networks)
            add_row = NetworkAddRow(networks, network_product_result, add_row_list)
            add_row_dict = add_row.group_list_to()
            network_add_route_update = NetworkProduct(network_builder_list_data,add_row_dict)
            networks_update = network_add_route_update.create_network_builder_list()
            network_add_route_update.product_networks(networks_update)
            return networks_update
        networks_update = create_chain_of_update()
        return networks_update


class NetworkProduct:
    def __init__( self, network_builder_list_data: list, add_row_dict: dict = None):
        """_summary_

        Args:
                network_builder_list_data (dict): list for NetworkBuilder creation
                input_list1 = [
                                polygon_merge,
                                (20000, 3000),
                                "S01",
                                "S_SA_fresh",
                                (-25000, 25000),
                                (3000, 3000),
                                "m_1",
                        ]

                network_add_route_update = NetworkProduct(
                [input_list1, input_list2, input_list3],add_row_dict,
                )
                add_row_dict (dict, optional): additional row for merge routes. Defaults to None.
                add_row = NetworkAddRow(networks,network_product_result,list_of_from_to)
                add_row_dict = add_row.group_list_to()

        Returns:
                dict: dictionary of additional row ->  product_networks

        """

        self.network_builder_list_data = network_builder_list_data
        self.add_row_dict = add_row_dict

    def create_network_builder_list(self,) -> list:
        """for make product and iteration on instance(add row)

        Returns:
                list: _description_
        """
        network_builder_list = [
            NetworkBuilder(
            polygon_merge = single_input_dict['polygon_merge'],
            system_location_point = single_input_dict['system_location_point'],
            system_name = single_input_dict['system_name'],
            sys_flow_column = single_input_dict['sys_flow_column'],
            network_coordinate_x = single_input_dict['network_coordinate_x'],
            network_coordinate_y = single_input_dict['network_coordinate_y'],
            route_name = single_input_dict['route_name'],
                add_row_dict=self.add_row_dict,
            )
            for single_input_dict in self.network_builder_list_data
        ]
        return network_builder_list

    @staticmethod
    def get_sub_combination_of_lists(iter_sublist):
        subres = []
        for sub_list in iter_sublist:
            if sub_list[0] != sub_list[1]:
                temp_val = sub_list[0] - sub_list[1]
                subres.append(temp_val)
        return subres

    @staticmethod
    def product_networks(network_builder_list: list) -> dict:
        list_of_date = network_builder_list
        join_list = list_of_date + list_of_date[::-1]
        res = list((combinations(join_list, 2)))
        NetworkProduct.get_sub_combination_of_lists(res)
        dict_of_add_row = {
            network.route_name: network.create_additional_route()
            for network in network_builder_list
        }
        return dict_of_add_row


class NetworkAddRow:
    def __init__(self, network_product_list_inst, network_product_result, list_of_from_to):
        self.network_product_list_inst = network_product_list_inst
        self.network_product_result = network_product_result
        self.list_of_from_to = list_of_from_to

    def group_list_to(self) -> dict:
        list_from = [sublist[0] for sublist in self.list_of_from_to]
        list_to = [sublist[1] for sublist in self.list_of_from_to]
        product_inst = self.network_product_result
        list_product_from = [product_inst[val] for val in list_from]
        list_for_group_by = [(x, y) for x, y in zip(list_to, list_product_from)]
        product_dict = collections.defaultdict(list)
        for key, group in list_for_group_by:
            product_dict[key].append(group)
        return product_dict

    def create_list_of_add_row(self) -> list:
        temp_list = []
        for inst_ in self.network_product_list_inst:
            temp_list.append(
                inst_.concate_additional_row_to_main_df(self.group_list_to())
            )
        return temp_list
