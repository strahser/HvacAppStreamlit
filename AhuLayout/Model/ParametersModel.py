from AhuLayout.Model.LabelsModel import *
import locale
locale.setlocale(locale.LC_ALL, '')
from library_hvac_app.list_custom_functions import flatten
from library_hvac_app.docx_custom_function import RenderDocx


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


