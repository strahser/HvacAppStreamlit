from dataclasses import dataclass, field, asdict
import pandas as pd

from Networks.CalculationNetwork.NetworkEngineer import ExcelQuery, SettingBuilder
from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel


@dataclass
class PressureModel:
	system_type: str
	from_branch: str
	to_branch: str
	distance: float = 10
	flow: float = 0
	diameter: int = 0
	velocity: float = 0
	Reynolds: float = 0
	lamda: float = 0
	line_pressure: float = 0
	full_line_pressure: float = 0
	dynamic_pressure: float = 0
	k_local_pressure: float = 0
	full_dynamic_pressure: float = 0
	calculated_pressure: float = 0
	additional_pressure: float = 0
	full_pressure: float = 0

	def calculate_pressure(self, power: float, input_settings_df: dict[str, pd.DataFrame]):
		excel_loader = ExcelQuery(self.system_type, input_settings_df)
		setting_builder = SettingBuilder(excel_loader, power, "root")
		self.flow = setting_builder.flow
		self.diameter = setting_builder.choose_standard_diameter()
		self.velocity = setting_builder.drop_pressure.get_velocity()
		self.Reynolds = setting_builder.drop_pressure.get_renolds_number()
		self.lamda = setting_builder.drop_pressure.get_lamda_turbulence()
		self.line_pressure = setting_builder.drop_pressure.get_pressure_line_drop()
		self.full_line_pressure = self.line_pressure * self.distance
		self.dynamic_pressure = setting_builder.drop_pressure.get_pressure_dynamic_drop()
		self.k_local_pressure = setting_builder.get_k_local_pressure()
		self.full_dynamic_pressure = self.dynamic_pressure * self.k_local_pressure
		self.calculated_pressure = self.full_line_pressure + self.full_dynamic_pressure
		self.full_pressure = self.calculated_pressure + self.additional_pressure

	def dict(self):
		return {k: v for k, v in asdict(self).items() if k not in ['branch_name']}
