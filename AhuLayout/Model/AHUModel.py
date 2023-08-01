import os
import inspect
import sys
from AhuLayout.Model.EquipmentModel import *

current_dir = os.path.dirname(
	os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)


class AHU:

	def __init__(self, df_setting: pd.DataFrame,
	             system_name: str, system_data: pd.DataFrame):
		self.list_ahu_property = None
		self.df_setting = df_setting
		self.system_name = system_name
		self.system_data = system_data.set_index("Result_index")
		self.columns = self.system_data.columns
		self.ahu_equipment: list[Equipment] = []
		self.en = 0

	def __repr__(self):
		return self.system_name

	def create_ahu(self):
		self.append_excel_input_table_to_ahu()
		for en, col in enumerate(self.columns):
			self.append_filters_to_ahu()
			self.append_exchanger_to_ahu()
			self.append_mix_up_equipment_to_ahu()
			self.append_standard_equipment_to_ahu()
			self.append_fan_to_ahu()
			self.en = en
		return self

	def append_exchanger_to_ahu(self):
		for exchanger in AHULabels.exchanger_dictionary.keys():
			he = HeatExchanger()
			he_data = he.append_exchangers_data_from_db(
				self.df_setting,
				exchanger,
				self.system_name,
				self.system_data,
				self.columns,
				self.en)
			self.ahu_equipment.append(he_data) if he_data else None
		return self

	def append_mix_up_equipment_to_ahu(self):
		mix_up_eq = MixUpEquipment()
		mix_up_eq_data = mix_up_eq.append_mix_up_data_from_db(
			self.system_name,
			self.system_data,
			self.columns,
			self.en)
		self.ahu_equipment.append(mix_up_eq_data) if mix_up_eq_data else None
		return self

	def append_fan_to_ahu(self):
		fan = Fan()
		add_fan = fan.append_fan_data_from_db(self.system_name,
		                                      self.system_data,
		                                      self.columns,
		                                      self.en)
		fan.calculate_fan_electric_power()
		self.ahu_equipment.append(add_fan) if add_fan else None
		return self

	def append_filters_to_ahu(self):
		filter_ = FilterAHU()
		filter_data = filter_.append_filters_data_from_db(
			self.system_name,
			self.system_data,
			self.columns,
			self.en)
		self.ahu_equipment.append(filter_data) if filter_data else None
		return self

	def append_standard_equipment_to_ahu(self):
		for equipment_name in AHULabels.standard_equipment_dictionary.keys():
			equipment = Equipment()
			eq = equipment.add_standard_equipment_data(self.system_data,
			                                           equipment_name,
			                                           self.system_name,
			                                           self.columns,
			                                           self.en)
			self.ahu_equipment.append(eq) if eq else None
		return self

	def append_excel_input_table_to_ahu(self):
		new_columns = [
			column_ for column_ in self.system_data.columns
			if "Unnamed" not in column_
		]
		self.excel_df = self.system_data[new_columns]
		return self.excel_df.fillna("")

	def create_list_ahu_property(self, system_name: str) -> pd.DataFrame:
		"""concat formatting air_parameters data """
		if self.system_name == system_name:
			list_ahu_property_ = []
			for ahu_equipment in self.ahu_equipment:
				list_ahu_property_.append(ahu_equipment.get_equipment_property())
			self.list_ahu_property = pd.concat(list_ahu_property_)
			return self.list_ahu_property.reset_index(drop=True).reset_index().fillna("")

	def create_ahu_labels_list(self, system_name: str, static_path: str = "static"):
		self.list_ahu_labels = []
		self.list_ahu_pictures = []
		for ahu_equipment in self.ahu_equipment:
			if ahu_equipment.system_name == system_name:
				self.list_ahu_labels.append(ahu_equipment.equipment_label)
				self.list_ahu_pictures.append(os.path.join(parent_dir, static_path, ahu_equipment.picture_name))
		return self.list_ahu_labels, self.list_ahu_pictures


class ListAHUModel:
	def __init__(self, df_ahu: pd.DataFrame):
		"""
		df_ahu:Excle AHU ->DF
		Args:
			df_ahu ():
		"""
		self.df_ahu = df_ahu
		self.list_ahu: list[AHU] = []

	def _create_filtered_excel(self):
		self.filtered_excel: dict[str:pd.DataFrame] = {
			k: v
			for k, v in self.df_ahu.items()
			if "Result_index" in v.columns and k != 'Расчет'
		}
		return self.filtered_excel

	def create_ahu_list(self, df_setting: pd.DataFrame) -> None:
		"""calculated ahu and create list AHU and AHU Table"""
		self._create_filtered_excel()
		for k, v in self.filtered_excel.items():
			ahu_ = AHU(df_setting, k, v)
			ahu_.create_ahu()
			ahu_.create_list_ahu_property(ahu_.system_name)
			ahu_.create_ahu_labels_list(ahu_.system_name)
			self.list_ahu.append(ahu_)
		return self.list_ahu


class HeatElectricalMarginsModel:
	def __init__(self, list_ahu: list[AHU]):
		self.list_ahu = list_ahu

	def __get_ahu_pivot_margins(self, heat_exchangers_names: list[str]):
		he_list = []
		electrical_list = []
		for ahu in self.list_ahu:
			for eq in ahu.ahu_equipment:
				if eq.equipment_name in heat_exchangers_names:
					power = eq.heat_exchanger_power
					he_list.append(power)
					electrical_list.append(eq.pump.electric_power)
				elif eq.equipment_name == "fan":
					electrical_list.append(eq.electric_power)
		return round(sum(he_list), 1), round(sum(electrical_list), 1)

	def get_heat_consumption(self):
		return self.__get_ahu_pivot_margins(["HE1", "HE2"])

	def get_cooling_consumption(self):
		return self.__get_ahu_pivot_margins(["CE1", "CE2"])

	def get_recuperation_consumption(self):
		return self.__get_ahu_pivot_margins(["RE1"])

	def get_fan_power(self):
		return self.__get_ahu_pivot_margins("")


class PivotTableAHUModel:
	def get_all_systems_names(self, df_revit: pd.DataFrame, system_columns_name: list[str]):
		all_systems = flatten([
			df_revit[column].dropna().unique().tolist()
			for column in system_columns_name
		])
		return all_systems

	@staticmethod
	def __add_equipment_for_pivot_table(ahu_property: list, ahu_inst: AHU) -> list[AHU]:
		if ahu_inst.equipment_name in AHULabels.exchanger_dictionary.keys():
			ahu_property.append(ahu_inst.concat_exchanger_and_pump_table())
		elif ahu_inst.equipment_name and "Filter_" in ahu_inst.equipment_name:
			ahu_property.append(ahu_inst.add_filter_table())
		elif ahu_inst.equipment_name and "fan" in ahu_inst.equipment_name:
			ahu_property.append(ahu_inst.add_fan_table())
		return ahu_property

	@staticmethod
	def append_ahu_spaces_to_ahu(
			df_revit: pd.DataFrame,
			system_name: str,
			system_columns_name: list[str],
			space_numbers_column_name: str = 'S_Number'):
		"""
		group spaces by system name system_columns_name
		 - name of column df with system name,space_data: str=S_Number
		 """
		res = []
		if space_numbers_column_name in df_revit.columns:
			for name in system_columns_name:
				filter_condition = df_revit[name] == system_name
				filter_condition_df = df_revit[filter_condition]
				group_data = filter_condition_df \
					.groupby(name, group_keys=False)[space_numbers_column_name] \
					.apply(tuple) \
					.reset_index()
				group_data[space_numbers_column_name] = group_data[space_numbers_column_name].apply(str)
				group_data = group_data.rename(
					{
						name: AHULabels.system_name,
						space_numbers_column_name: AHULabels.space_name
					},
					axis=1)
				group_data = group_data.set_index(AHULabels.system_name)
				res.append(group_data)
			concat_data = pd.concat(res)
			concat_data.columns = [[AHULabels.space_property], [AHULabels.space_name]]
			return concat_data

	def get_ahu_pivot_table(self, ahu_: AHU, df_revit, system_columns_name,
	                        space_numbers_column_name: str = 'S_Number'):
		ahu_property = []
		list_ahu_table = []
		for eq in ahu_.ahu_equipment:
			self.__add_equipment_for_pivot_table(ahu_property, eq)
			ahu_spaces = self.append_ahu_spaces_to_ahu(df_revit, ahu_.system_name, system_columns_name,
			                                           space_numbers_column_name)
		df_merged = ahu_spaces.join(ahu_property[0].join(ahu_property[1:]), how='right').reset_index()
		list_ahu_table.append(df_merged)
		res = pd.concat(list_ahu_table).fillna(0).reset_index(drop=True)
		return res
