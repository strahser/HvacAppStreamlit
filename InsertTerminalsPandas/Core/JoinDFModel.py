from InsertTerminalsPandas.InputData.input import *
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing


class JoinRevitExportTerminalsSheets:
	def __init__(self, system_type, input_data_df: InputDataDF):
		"""join spaces and device property's(excel sheets devices,device_type and revit_export)

        Args:
            system_type (str): _description_

        Returns:
        Returns:
            pd.DataFrame: _description_
        """
		self.system_type = system_type
		self.exclude_columns = input_data_df.system_dictionary.keys()
		self.input_data_df = input_data_df

	def join_devices(self) -> pd.DataFrame:
		"""join bases devices and device_type
        """
		devices_df = self.input_data_df.devices
		devices_df[ColumnChoosing.S_ID] = devices_df[ColumnChoosing.S_ID].astype("string")
		terminal_base = devices_df \
			.filter([ColumnChoosing.S_ID, self.system_type]) \
			.merge(self.input_data_df.device_type, how='left', left_on=self.system_type,
		           right_on=ColumnChoosing.type_index) \
			.drop(self.system_type, axis=1)
		return terminal_base

	def join_spaces_and_devices(self, input_data_df_table) -> pd.DataFrame:
		"""join spaces,devices

        Returns:
            pd.DataFrame: _description_
        """
		joined_devices = self.join_devices()
		revit_export = self.input_data_df.revit_export
		revit_export[ColumnChoosing.S_ID] = revit_export[ColumnChoosing.S_ID].astype("string")
		joined_df = revit_export.merge(joined_devices, how='left', on=ColumnChoosing.S_ID)
		return joined_df
