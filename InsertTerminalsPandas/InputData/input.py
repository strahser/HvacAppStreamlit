from collections import namedtuple
import pandas as pd
import streamlit as st

import SQL.SqlModel.SqlConnector
from InsertTerminalsPandas.Static.CalculationOptions import CalculationOptions
from Session.StatementConfig import StatementConstants
from Upload.UploadLayout import UploadLayout
from InputView.InputViewMultyChoosing import InputViewMultyChoosing
from StaticData.AppConfig import ExcelSheetsLoads
from InsertTerminalsPandas.Static.DevicePropertiesName import DevicePropertiesName
from StaticData.AppConfig import MenuChapters

SystemProperty = namedtuple('SystemProperty', ['system_flow', 'system_name'])


class InputDataDF:

	def __init__(self, upload_layout: UploadLayout, ):
		self.upload_layout = upload_layout
		self.json_data = upload_layout.json_file
		self.revit_export = None
		self.EquipmentBase = []
		self.devices = None
		self.device_type = None
		self.config = None
		self.device_orientation = None
		self.device_property_columns_names = None
		self.additional_columns = None
		self.calculation_options = None
		self.json_df_columns = None
		self.df_device_result_columns = None
		self.system_dictionary = None
		self.unique_terminals = None

	def show_form(self):
		view_multiprocessing = InputViewMultyChoosing(self.upload_layout, key=MenuChapters.terminals)
		view_multiprocessing.check_input_data_loaded(
			ExcelSheetsLoads.excel_sheet_names_Terminal,
			StatementConstants.terminal_names_dict
		)

	def create_config_data(self):
		self.concat_base = pd.concat(self.EquipmentBase)
		self.unique_terminals = self.concat_base.family_device_name.unique()
		self.config = self.config.to_dict('records')
		self.system_dictionary = {
			records['system_type']: SystemProperty(records['system_flow'], records['system_name']) for records in
			self.config
		}
		self.df_device_result_columns = DevicePropertiesName.df_device_result_columns
		self.json_df_columns = DevicePropertiesName.json_df_columns
		self.calculation_options = DevicePropertiesName.calculation_options
		self.device_property_columns_names = DevicePropertiesName.device_property_columns_names
		self.additional_columns = DevicePropertiesName.additional_columns \
		                          + self.device_property_columns_names \
		                          + self.calculation_options
