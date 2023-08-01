from AhuLayout.Model.ParametersModel import *
# region data Equipment
def _read_air_parameters_from_db(db_table: pd.DataFrame,
                                 key_db_column_name: str) -> AirParameters:
	air_parameter = AirParameters()
	for parameter in AirParameters.__annotations__.keys():
		set_attr_air_in = db_table.loc[
			getattr(LabelAirParameters, parameter), key_db_column_name]
		setattr(air_parameter, parameter, set_attr_air_in)
	return air_parameter


@dataclass
class Equipment:
	system_name: str = None
	equipment_name: str = None
	equipment_label: str = None
	key_parameter_in: str = None
	key_parameter_out: str = None
	picture_name: str = None
	heat_exchanger_power: float = None
	air_parameters_in: AirParameters = field(default_factory=AirParameters)
	air_parameters_out: AirParameters = field(default_factory=AirParameters)
	air_mixing_result: AirParameters = field(default_factory=AirParameters)

	def add_standard_equipment_data(self, system_data: pd.DataFrame,
	                                equipment_name: str, system_name: str,
	                                columns: list[str], en: int):
		if equipment_name in columns[en]:
			self.system_name = system_name
			self.equipment_name = equipment_name
			self.picture_name = f"{equipment_name}.jpg"
			self.equipment_label = AHULabels.standard_equipment_dictionary[
				equipment_name]
			self.key_parameter_in = equipment_name
			self.key_parameter_out = equipment_name
			self.air_parameters_in = _read_air_parameters_from_db(
				system_data, self.key_parameter_in)
			self.air_parameters_out = _read_air_parameters_from_db(
				system_data, self.key_parameter_in)
			return self

	def get_equipment_property(self) -> pd.DataFrame():
		"""formatting air_parameters_in"""
		data = [
			self.system_name, self.equipment_label,
			round(self.air_parameters_in.temperature_air,
			      1), f"{self.air_parameters_in.relative_humidity:.2%}",
			f"{self.air_parameters_in.volume_air_consumption:,.0f}".replace(
				',', ' '),
			round(self.air_parameters_out.temperature_air,
			      1), f"{self.air_parameters_out.relative_humidity:.2%}",
			f"{self.air_parameters_out.volume_air_consumption:,.0f}".replace(
				',', ' '),
			round(self.heat_exchanger_power)
			if self.heat_exchanger_power else None
		]

		columns = [
			AHULabels.system_name, AHULabels.equipment_name,
			AHULabels.temperature_air_in, AHULabels.relative_humidity_in,
			AHULabels.air_flow_in, AHULabels.temperature_air_out,
			AHULabels.relative_humidity_out, AHULabels.air_flow_out,
			AHULabels.heat_exchanger_power
		]
		dict_data = {k: [v] for k, v in zip(columns, data)}
		df = pd.DataFrame(dict_data)

		return df


@dataclass
class Pump:
	system_name: str = None
	equipment_name: str = None
	equipment_label: str = PumpLabels.equipment_name
	pump_flow: float = None
	heat_power: float = 0
	electric_power: float = 0
	pressure: float = 10
	efficiency: float = 0.8

	def calculate_pump_flow(self, liquid_parameters: LiquidParameters):
		temperature_liquid_in: float = liquid_parameters.temperature_liquid_in
		temperature_liquid_out: float = liquid_parameters.temperature_liquid_out
		density_liquid: float = liquid_parameters.density_liquid
		heat_capacity: float = liquid_parameters.heat_capacity
		pump_flow: float = 3.6 * self.heat_power / (
				(temperature_liquid_in - temperature_liquid_out) * density_liquid *
				heat_capacity)
		pump_flow = pump_flow if pump_flow > 0 else pump_flow * (-1)
		self.pump_flow = round(pump_flow, 1)
		return self.pump_flow

	def calculate_pump_electric_power(self,
	                                  liquid_parameters: LiquidParameters,
	                                  electric_power: float = 0):
		if electric_power:
			self.electric_power = electric_power
			return self.electric_power
		else:
			density_liquid: float = liquid_parameters.density_liquid
			self.electric_power = (1.1 * self.pump_flow / 3600 *
			                       density_liquid * self.pressure *
			                       10) / self.efficiency * 0.9
		return self.electric_power


@dataclass
class HeatExchanger(Equipment):
	heat_exchanger_power: float = None
	temperature_air_in: float = None
	temperature_air_out: float = None
	pump: Pump = None

	def calculate_heat_exchanger_power(self, air_flow: float = 0) -> float:
		if air_flow:
			delta_enthalpy = self.air_parameters_out.enthalpy - self.air_parameters_in.enthalpy
			self.heat_exchanger_power = delta_enthalpy * air_flow / 3000
		else:
			self.heat_exchanger_power = self.air_parameters_out.power

		self.temperature_air_in = self.air_parameters_in.temperature_air
		self.temperature_air_out = self.air_parameters_out.temperature_air
		return self.heat_exchanger_power

	def add_liquid_parameters_from_db(
			self,
			setting_df: pd.DataFrame,
	) -> LiquidParameters:

		query = setting_df[LiquidAttributes.liquid_attributes['system_column_name']] == self.equipment_name
		df = setting_df[query]
		if not df.empty and self.equipment_name in AHULabels.exchanger_dictionary.keys():
			self.liquid_parameter = LiquidParameters()
			self.liquid_parameter.equipment_name = self.equipment_name
			for liquid, setting in LiquidAttributes.liquid_attributes.items():
				setattr(self.liquid_parameter, liquid, df[setting].tolist()[0])
			return self.liquid_parameter

	def add_pump(self, liquid_parameters: LiquidParameters) -> Pump:
		self.pump = Pump()
		self.pump.system_name = self.system_name
		self.pump.heat_power = self.heat_exchanger_power
		self.pump.calculate_pump_flow(liquid_parameters)
		self.pump.calculate_pump_electric_power(liquid_parameters)
		self.pump.equipment_name = f"{self.equipment_name}"
		return self.pump

	def append_exchangers_data_from_db(self, df_setting: pd.DataFrame,
	                                   key_parameter: str, system_name: str,
	                                   system_data: pd.DataFrame,
	                                   columns: list[str],
	                                   en: int) -> Equipment:
		if en < len(columns) - 1:
			check_input_air_parameters = f"{key_parameter}_in" == columns[en]
			check_output_air_parameters = f"{key_parameter}_out" == columns[en
			                                                                +
			                                                                1]
			if check_input_air_parameters and check_output_air_parameters:
				self.system_name = system_name
				self.equipment_label = AHULabels.exchanger_dictionary[
					key_parameter]
				self.key_parameter_in = f"{key_parameter}_in"
				self.key_parameter_out = f"{key_parameter}_out"
				self.equipment_name = key_parameter
				self.picture_name = f"{key_parameter}.jpg"
				self.air_parameters_in = _read_air_parameters_from_db(
					system_data, self.key_parameter_in)
				self.air_parameters_out = _read_air_parameters_from_db(
					system_data, self.key_parameter_out)
				self.calculate_heat_exchanger_power()
				self.add_liquid_parameters_from_db(df_setting)
				self.add_pump(self.liquid_parameter)
				self.pump.calculate_pump_electric_power(self.liquid_parameter)
				return self

	def add_exchanger_table(self) -> pd.DataFrame():
		colspan_column = f"{self.equipment_label} {self.equipment_name}"
		equipment_columns = [
			AHULabels.temperature_air_in, AHULabels.temperature_air_out,
			AHULabels.heat_exchanger_power
		]
		multicolumns = pd.MultiIndex.from_product([[colspan_column],
		                                           equipment_columns])
		data = [
			self.air_parameters_in.temperature_air,
			self.air_parameters_out.temperature_air, self.heat_exchanger_power
		]
		dict_data = {k: [v] for k, v in zip(multicolumns, data)}
		df = pd.DataFrame(dict_data, index=[self.system_name])
		df.index.name = AHULabels.system_name
		return df

	def add_exchanger_pump_table(self) -> pd.DataFrame():
		data = [
			self.pump.pump_flow, self.pump.electric_power, self.pump.pressure
		]
		colspan_column = f"{self.pump.equipment_label} {self.equipment_name}"
		equipment_columns = [
			PumpLabels.pump_flow, PumpLabels.electric_power,
			PumpLabels.pressure
		]
		multicolumn = pd.MultiIndex.from_product([[colspan_column],
		                                          equipment_columns])
		dict_data = {k: [v] for k, v in zip(multicolumn, data)}
		df = pd.DataFrame(dict_data, index=[self.system_name])
		df.index.name = AHULabels.system_name
		return df

	def concat_exchanger_and_pump_table(self) -> pd.DataFrame():
		res = self.add_exchanger_table().join(self.add_exchanger_pump_table())
		return res


@dataclass
class Fan(Equipment):
	key_parameter_in: str = "fan"
	electric_power: float = 0
	fan_pressure: float = 300
	fan_explosion_protection: str = AHULabels.fan_explosion_protection

	def append_fan_data_from_db(self, system_name: str,
	                            system_data: pd.DataFrame, columns: list[str],
	                            en: int):
		check_input_parameters = self.key_parameter_in in columns[en]
		if check_input_parameters:
			self.system_name = system_name
			self.equipment_name = self.key_parameter_in
			self.picture_name = f"{self.equipment_name}.jpg"
			self.equipment_label = AHULabels.fan_name
			self.air_parameters_in = _read_air_parameters_from_db(
				system_data, self.key_parameter_in)
			self.air_parameters_out = _read_air_parameters_from_db(
				system_data, self.key_parameter_in)
			return self

	def calculate_fan_electric_power(self, electric_power: float = 0) -> float:
		if electric_power:
			self.electric_power = electric_power
			return self.electric_power
		elif self.air_parameters_in.volume_air_consumption and self.fan_pressure:
			self.electric_power = round(
				self.air_parameters_in.volume_air_consumption *
				self.fan_pressure / (3.6 * 10 ** 6 * 0.85), 1)
			return self.electric_power
		else:
			return 0

	def add_fan_table(self) -> pd.DataFrame():
		colspan_column = f"{AHULabels.fan_name}"
		equipment_columns = [
			AHULabels.volume_air_consumption, AHULabels.fan_pressure,
			AHULabels.electric_power, AHULabels.fan_explosion_protection_label
		]
		multicolumns = pd.MultiIndex.from_product([[colspan_column],
		                                           equipment_columns])
		data = [
			self.air_parameters_in.volume_air_consumption, self.fan_pressure,
			self.electric_power, self.fan_explosion_protection
		]
		dict_data = {k: [v] for k, v in zip(multicolumns, data)}
		df = pd.DataFrame(dict_data, index=[self.system_name])
		df.index.name = AHULabels.system_name
		return df


@dataclass
class FilterAHU(Equipment):
	key_parameter: str = "Filter_"
	filter_type: str = ""

	def append_filters_data_from_db(self, system_name: str, system_data: pd.DataFrame,
	                                columns: list[str],
	                                en: int):
		check_input_parameters = self.key_parameter in columns[en]
		if check_input_parameters:
			self.system_name = system_name
			self.filter_type = columns[en].split("_")[1]
			self.equipment_label = f"{AHULabels.filter_name} {self.filter_type}"
			self.equipment_name = self.key_parameter + self.filter_type
			self.picture_name = f"{self.equipment_name}.jpg"
			self.air_parameters_in = _read_air_parameters_from_db(
				system_data, self.equipment_name)
			self.air_parameters_out = _read_air_parameters_from_db(
				system_data, self.equipment_name)
			return self

	def add_filter_table(self) -> pd.DataFrame():
		colspan_column = f"{AHULabels.filter_name}"
		equipment_columns = [self.filter_type]
		multicolumn = pd.MultiIndex.from_product([[colspan_column],
		                                          equipment_columns])
		data = [self.filter_type]
		dict_data = {k: [v] for k, v in zip(multicolumn, data)}
		df = pd.DataFrame(dict_data, index=[self.system_name])
		df.index.name = AHULabels.system_name
		return df


@dataclass
class MixUpEquipment(Equipment):
	equipment_name: str = "Mix_up"
	key_parameter_in: str = 'Mix_up1'
	key_parameter_out: str = 'Mix_up2'
	key_parameter_mixing_result: str = "Mix_up_result"
	picture_name: str = "Mix_up.jpg"

	def __check_columns_db_minimum_count(self, columns: list[str], en: int) -> bool:
		if en < len(columns) - 2:
			check_in_air_parameters = self.key_parameter_in == columns[en]
			check_out_air_parameters = self.key_parameter_out == columns[en + 1]
			check_air_mixing_result = self.key_parameter_mixing_result == columns[en + 2]
			self.equipment_label = AHULabels.mix_up
			condition = check_in_air_parameters and check_out_air_parameters and check_air_mixing_result
			return condition

	def _read_mix_up_air_parameters_from_db(self, system_name: str, system_data: pd.DataFrame):
		self.system_name = system_name
		self.air_parameters_in = _read_air_parameters_from_db(system_data, self.key_parameter_in)
		self.air_parameters_out = _read_air_parameters_from_db(system_data, self.key_parameter_out)
		self.air_mixing_result = _read_air_parameters_from_db(system_data, self.key_parameter_mixing_result)

	def append_mix_up_data_from_db(self, system_name: str, system_data: pd.DataFrame, columns: list[str],
	                               en: int) -> Equipment:
		condition = self.__check_columns_db_minimum_count(columns, en)
		if condition:
			self._read_mix_up_air_parameters_from_db(system_name, system_data)
			return self


# 	endregion
