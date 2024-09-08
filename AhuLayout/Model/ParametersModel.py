from AhuLayout.Model.LabelsModel import *
from dataclasses import dataclass, field
import locale

locale.setlocale(locale.LC_ALL, '')


@dataclass
class LiquidParameters:
	equipment_name: str = None
	temperature_liquid_in: float = 90
	temperature_liquid_out: float = 70
	density_liquid: float = 1000
	heat_capacity: float = 4200


@dataclass
class AirParameters:
	temperature_air: float = 0
	relative_humidity: float = 0
	temperature_liquid: float = 0
	enthalpy: float = 0
	density_air: float = 0
	temp_wet_term: float = 0
	mass_air_consumption: float = 0
	volume_air_consumption: float = 0
	power: float = 0
	wet_power: float = 0
