from AhuLayout.Model.AHUModel import AHU,HeatElectricalMarginsModel
from AhuLayout.Model.ParametersModel import BuildingHeatCoolLabel
import streamlit as st
import pandas as pd


class TotalDataConsumptionModel:
	@staticmethod
	def create_margins_table_view(ahu_list: list[AHU]):
		margins = HeatElectricalMarginsModel(ahu_list)
		electrical_power = margins.get_heat_consumption()[1] + \
		                   margins.get_cooling_consumption()[1] + \
		                   margins.get_recuperation_consumption()[1] + \
		                   margins.get_fan_power()[1]

		init_dict = {label.value: [0] for label in BuildingHeatCoolLabel}
		init_dict.update(
			{
				BuildingHeatCoolLabel.heat_ventilation_power.value: [margins.get_heat_consumption()[0]],
				BuildingHeatCoolLabel.cooling_total_power.value: [margins.get_cooling_consumption()[1]],
				BuildingHeatCoolLabel.electrical_engin_power.value: [electrical_power]
			}
		)
		if "df_data_ahu_load" not in st.session_state: st.session_state["df_data_ahu_load"] = {}
		df_ = pd.DataFrame(init_dict) if not st.session_state["df_data_ahu_load"] \
			else pd.DataFrame(st.session_state["df_data_ahu_load"])

		df_[BuildingHeatCoolLabel.heat_total_power.value] = df_[BuildingHeatCoolLabel.heat_total_power.value].apply(
			lambda df: TotalDataConsumptionModel. \
				_calculate_total_sum(
				df_[BuildingHeatCoolLabel.heat_ventilation_power.value],
				df_[BuildingHeatCoolLabel.heat_heating_power.value],
				df_[BuildingHeatCoolLabel.heat_water_power.value]
			)
		)
		return df_

	@staticmethod
	def _calculate_total_sum(vent_power: float, heating_power: float, hot_water_power: float):
		res = float(vent_power) + float(heating_power) + float(hot_water_power)
		return res