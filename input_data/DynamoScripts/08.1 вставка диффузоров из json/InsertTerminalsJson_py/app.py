# -*- coding: utf-8 -*-
# methods from dynamo Revit v 2020.2

import os
import sys

path_to_current_file = IN[0]
json_path = str(UnwrapElement(IN[1]))

curent_dir = os.path.dirname(str(path_to_current_file))
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(os.path.dirname(str(path_to_current_file)))
from InsertTerminalsFunctions import *



class ReadJson:
    def __init__(self, path_to_json):
        self.path_to_json = path_to_json

    def get_json_data(self):
        return open_json(self.path_to_json)


class ParseJson:
    def __init__(self, json_data):
        """Convert input dictionary to class add family instance.Convert points to DS points.
            convert family instance name to family instance.
        for key in json_data.keys():
            setattr(self,key,json_data[key])
        """
        self.json_data = json_data
        self.S_ID = json_data["S_ID"]
        self.family_device_name = json_data["family_device_name"]
        self.family_instance_name = json_data["family_instance_name"]
        self.minimum_device_number = json_data["minimum_device_number"]
        self.flow_to_device_calculated = json_data["flow_to_device_calculated"]
        self.system_name = json_data["system_name"]
        self.sys_flow_parametr_name = json_data['sys_flow_parametr_name']
        self.sys_name_parametr = json_data['sys_name_parametr']
        self.instance_points = self._convert_to_DS_points()

    def _convert_to_DS_points(self):
        points_list = []
        if not isinstance(self.json_data["instance_points"][0], list):
            return Point.ByCoordinates(*self.json_data["instance_points"])

        else:
            for points in self.json_data["instance_points"]:
                points_list.append(Point.ByCoordinates(*points))

        return points_list

    def get_family_instance(self):
        self.family_instance = FamilyType(
            self.family_device_name, self.family_instance_name).get_filtred_family_type()
        return self.family_instance


class FamilyType:

    def __init__(self, family_device_name, instance_type_name):
        """get DS family instance by family name, and instance name
        Args:
            family_device_name (str): _description_
            instance_type_name (str): _description_
        """
        self.family_device_name = family_device_name
        self.instance_type_name = instance_type_name

    def get_family(self):
        return Revit.Elements.Family.ByName(self.family_device_name)

    def _get_all_family_types(self):
        if self.get_family():
            return self.get_family().Types
        else:
            raise Exception("Wrong family Type Name")

    def get_filtred_family_type(self):
        for family in self._get_all_family_types():
            if family.Name == self.instance_type_name:
                return family


class InsertTerminalByPoint:
    def __init__(self, pars_json):
        """insert one family instance to several points

        Args:
            family_instance (family type: DS family type
            points (points): DS points
            pars_json:ParseJson
        """
        self.family_instance = pars_json.get_family_instance()
        self.points = tolist(pars_json.instance_points)
        self.sys_flow_parametr_name = pars_json.sys_flow_parametr_name
        self.sys_name_parametr = pars_json.sys_name_parametr
        self.flow_to_device_calculated = pars_json.flow_to_device_calculated
        self.system_name = pars_json.system_name

    def _add_system_name_and_flow_to_terminal(self,insert_terminal):
        # parametr = insert_terminal.GetParameterValueByName(self.sys_flow_parametr_name)
        # ProjectUnits = parametr.DisplayUnitType
        # newval = UnitUtils.ConvertToInternalUnits(self.flow_to_device_calculated, ProjectUnits)

        Revit.Elements.Element.SetParameterByName(
                insert_terminal, self.sys_flow_parametr_name, float(self.flow_to_device_calculated))
        Revit.Elements.Element.SetParameterByName(
                insert_terminal, self.sys_name_parametr, self.system_name)


    def insert_instance_by_family(self):
        instance_list = []
        for point in self.points:
            insert_terminal = Revit.Elements.FamilyInstance.ByPoint(
                self.family_instance, point)            
            instance_list.append(insert_terminal)
        return instance_list


class Main:
    def __init__(self, json_path):
        self.json_data = ReadJson(json_path).get_json_data()

    def insert_all_terminals(self):
        list_of_terminals = []
        exception_lsit = []
        for data in self.json_data:
            json_ = ParseJson(data)
            try:
                terminal = InsertTerminalByPoint(json_)
                list_of_terminals.append(terminal.insert_instance_by_family())
            except:
                exception_lsit.append(json_.family_instance_name)
        return list_of_terminals,exception_lsit

OUT = Main(json_path).insert_all_terminals()
