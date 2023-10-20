from dataclasses import dataclass, field, asdict
import pandas as pd
import datetime


@dataclass
class NetworkBranchModel:
	system_name: str
	system_type: str
	system_level: str
	network_draft_plot_data: str | object
	network_pressure_plot_data: str | object
	network_long_plot_data: str | object
	network_pressure_table: pd.DataFrame | dict
	network_long_pressure_table: pd.DataFrame | dict
	network_draft_plot_name: str = "Draft plot"
	network_pressure_plot_name: str = "Pressure plot"
	network_long_plot_name: str = "Long Pressure plot"
	network_table_pressure_name: str = "Pressure drop calculation"
	network_table_main_route_pressure_name: str = "Main route Pressure drop calculation"
	branch_name: str = field(init=False)
	data_create: str = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}'

	def __post_init__(self):
		self.branch_name = f"{self.system_name}_{self.system_level}"

	def dict(self):
		return {k: v for k, v in asdict(self).items() if k not in ['branch_name']}

	@property
	def max_pressure(self):
		df = pd.DataFrame(self.network_long_pressure_table)
		return df["full_pressure"].sum()

	@property
	def max_flow(self):
		df = pd.DataFrame(self.network_long_pressure_table)
		return df["flow"].max()
