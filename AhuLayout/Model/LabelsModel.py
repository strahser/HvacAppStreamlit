
from enum import Enum


# region data Labels

class AHULabels:
	# can be changed
	system_name: str = "Система"
	space_property: str = "Характеристика помещиния"
	space_name: str = "Наименование обслуживаемого помещения"
	equipment_name: str = "Наименование оборудования"
	heat_exchanger_power: str = "Тепл./холод. Мощ.,кВт"
	temperature_air_in: str = "Т вх.,С"
	air_flow_in: str = "Расход в-ха вход."
	temperature_air_out: str = "Т ис,С"
	relative_humidity_in: str = "Относ.влажность.вход."
	relative_humidity_out: str = "Относ.влажность.исход."
	air_flow_out: str = "Расход в-ха исх."
	volume_air_consumption: str = 'L,м3/ч'
	filter_name: str = "Фильтр"
	fan_name: str = "Вентилятор"
	fan_pressure: str = "Р,Па"
	fan_explosion_protection_label: str = "Взрывозащита"
	fan_explosion_protection: str = "Обычный"
	electric_power: str = "N,кВт"
	#  label for table of equipment property values can be changed,keys can NOT be changed
	exchanger_dictionary = dict(HE1="Тепл.нагрев.",
	                            HE2="Тепл.нагрев.",
	                            CE1="Тепл.охлажд.",
	                            CE2="Тепл.охлажд.",
	                            RE1="Тепл.рекуп.")
	standard_equipment_dictionary = dict(
		air_in_left="Забор в-ха лево",
		air_in_up="Забор в-ха верх",
		air_out_right="Забор в-ха право",
		air_out_up="Выброс  верх",
		silencer="Шумоглушитель",
		humiditer="Увлажнитель воздуха",
	)
	mix_up = "Камера Смешения"


class PumpLabels:
	system_name: str = "Система"
	equipment_name: str = "Насос"
	pump_flow: str = "G, м3/час"
	electric_power: str = "N,кВт"
	pressure: str = "Р,м.в.ст"


class LabelAirParameters:
	# do NOT change! names  as Excel file have to be
	temperature_air: str = 'Температура'
	relative_humidity: str = 'Отн. влажность'
	temperature_liquid: str = 'Абс. влажность'
	enthalpy: str = 'Энтальпия'
	density_air: str = 'Плотность'
	temp_wet_term: str = 'Тем.влажн.терм.'
	mass_air_consumption: str = 'Расход'
	volume_air_consumption: str = 'Расход*'
	power: str = 'Мощность'
	wet_power: str = 'Влагоприток'


class LiquidAttributes:
	# populate with Excel setting sheet db keys can NOT be changed!
	liquid_attributes: dict = {
		"density_liquid": "density",
		"temperature_liquid_in": "t_max",
		"temperature_liquid_out": "t_min",
		"heat_capacity": "heat_capacity",
		"system_column_name": "short_sys_type"
	}


class InputTableLabels:
	ahu_equipment_table_name = "Конфигурация приточной установки"
	ahu_equipment_property = "Характеристика приточной установки"
	filter_pivot_table = "Состав приточной установки"
	filtered_spaces_tabel = "Помещения которые обслуживает установка"
	heading = 'Характеристики системы'


class BuildingHeatCoolLabel(Enum):
	building_name: str = "Наименование Здания"
	building_volume: str = "Объем"
	year_periods: str = "Периоды года, при tн"
	# heat_power: str = "Расход теплоты кВт"
	heat_heating_power: str = "На отопление кВт"
	heat_ventilation_power: str = "На вентиляцию кВт"
	heat_water_power: str = "На горячее водоснабжение кВт"
	heat_total_power: str = "Итого расход теплоты кВт"
	cooling_total_power: str = "Расход холода Вт"
	electrical_engin_power: str = "Мощность элект.дв. кВт"



# endregion
