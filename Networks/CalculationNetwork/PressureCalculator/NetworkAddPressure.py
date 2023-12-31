import pandas as pd

from Networks.CalculationNetwork.NetworkBuilder import NetworkBuilder
from Networks.CalculationNetwork.NetworkEngineer import SettingBuilder
from Networks.CalculationNetwork.NetworkEngineer import ExcelQuery
from Networks.CalculationNetwork.StaticData.NetworkPressureConstants import NetworkPressureConstants
from Networks.CalculationNetwork.utility import p_distance, segment_center
from library_hvac_app.list_custom_functions import to_list


class NetworkAddPressure:
	def __init__(
			self,
			excel_loader: ExcelQuery,
			network: NetworkBuilder,
			df_branch: pd.DataFrame,
			prefix_from: str,
	) -> None:
		"""Adds calculated pressure drop columns,
        reorganizes the columns of branches and the main path connects the tables
        of branches and trunk, reinserts the resulting columns

        Args:
            network (NetworkCreataorControl): [description]
            sys_name (str): [description]
            rout_name_prefix (str): [description]
        """
		self.prefix_from = to_list(prefix_from)
		self.excel_loader = excel_loader
		self.network = network
		self.df = df_branch
		self.new_columns = NetworkPressureConstants.new_columns

	def _get_distance_column_name(self, root_type):
		if root_type == "branch":
			return self.network.branch_dist
		else:
			return self.network.rout_dist

	def _get_flow_column_name(self, root_type):
		if root_type == "branch":
			return self.network.sys_flow_column
		else:
			return self.network.sum_column

	def _get_columns_names(self, root_type):
		if root_type == "branch":
			return NetworkPressureConstants.branch_columns
		else:
			return NetworkPressureConstants.route_columns

	def get_old_columns_names(self, root_type):
		old_columns = [
			getattr(self.network, val) for val in self._get_columns_names(root_type)
		]
		return old_columns

	def _get_rename_columns_names(self, root_type):

		old_columns = [
			getattr(self.network, val) for val in self._get_columns_names(root_type)
		]
		rename_columns = dict(zip(old_columns, self.new_columns))
		return rename_columns

	def apply_to_coordinate_column(self, root_type):
		df = self.df
		if root_type == "branch":
			df = df.assign(to_x=self.df[self.network.x_intersect])
			df = df.assign(to_y=self.df[self.network.y_intersect])
		else:
			df = df.assign(to_x=self.df[self.network.x_intersect].shift(-1))
			df = df.assign(to_y=self.df[self.network.y_intersect].shift(-1))
		return df

	def rename_df_columns(self, root_type):
		df = self.apply_to_coordinate_column(root_type)
		old_columns = self.get_old_columns_names(root_type)
		rename_columns = dict(zip(old_columns, self.new_columns))
		df = df.rename(columns=rename_columns)

		return df

	def apply_location_point_coordinates(self, root_type):
		df = self.rename_df_columns(root_type)
		mask = df["to"].str.contains("cent", regex=False) & df["to_x"].isna()
		df.loc[mask, "to_x"] = self.network.system_location_point[0]
		df.loc[mask, "to_y"] = self.network.system_location_point[1]
		return df

	def get_root_distance(self, root_type):
		df = self.apply_location_point_coordinates(root_type)
		df = df.assign(
			distance=df.apply(
				lambda x: round(
					p_distance(x["from_x"], x["from_y"], x["to_x"], x["to_y"])
				)
				          / 1000,
				axis=1,
			)
		)
		return df

	def get_center_line_coordinates(self, df):
		"""df with 'from_x' 'to_x' 'from_y' 'to_y' columns for plote

        Args:
            df (_type_): _description_

        Returns:
            _type_: _description_
        """
		df = df.assign(
			center_x=df.apply(lambda x: segment_center(x["from_x"], x["to_x"]), axis=1)
		)
		df = df.assign(
			center_y=df.apply(lambda x: segment_center(x["from_y"], x["to_y"]), axis=1)
		)
		return df

	def drop_null_distance(self, root_type):
		df = self.get_root_distance(root_type)
		mask = df["distance"] > 0
		df = df.loc[mask]
		return df

	def get_pressure_data_column(self, power: float, network_branch_type: str):
		"""calculation of diameter, velocity, pressure loss along length and dynamic pressure loss

        Args:
            power (float): [power or flow]
            sys_type (str): [heating,ventilation from excel table]
            root_type (str): [branch or main. for velocity setting]

        Returns:
            [dict]: [main diam,veloc,pressure loss]
        """
		seting_builder = SettingBuilder(self.excel_loader, power, network_branch_type)
		drop_pressure = seting_builder.drop_pressure
		k_local_pressure = seting_builder.get_k_local_pressure()
		if power == 0:
			return dict(
				flow=None,
				diameter=None,
				velocity=None,
				line_pressure=None,
				dinamic_pressure=None
			),
		else:
			return dict(
				flow=seting_builder.flow,
				diameter=seting_builder.choose_standard_diameter(),
				velocity=drop_pressure.get_velocity(),
				line_pressure=drop_pressure.get_pressure_line_drop(),
				dinamic_pressure=drop_pressure.get_full_dynamic_drop_pressure(k_local_pressure)
			)

	def _apply_pressure_data_columns(self, root_type):
		"""apply 'flow','diameter','velocity', 'line_pressure', 'dinamic_pressure'
        to df.

        Args:
            root_type ([str]): [branch,any]

        Returns:
            [pd]: [description]
        """
		df = self.get_root_distance(root_type)
		df["seting_builder"] = df.apply(lambda x: SettingBuilder(self.excel_loader, x["power"], root_type), axis=1)
		for key, val in NetworkPressureConstants.calculation_dict.items():
			df[key] = df.apply(val, axis=1)
		df = df.drop(columns="seting_builder")
		df = df.assign(full_line_pressure=df["distance"] * df["line_pressure"])
		df = df.assign(full_pressure=df["full_line_pressure"] + df["dinamic_pressure"])
		if df["power"].equals(df["flow"]):
			df = df.drop(columns="flow")
			df = df.rename(columns={"power": "flow"})
		return df

	def concate_df(self):
		df_branch = self._apply_pressure_data_columns("branch")
		df_root = self._apply_pressure_data_columns("root")
		concate_df = pd.concat([df_branch, df_root], ignore_index=True)
		concate_df = self.get_center_line_coordinates(concate_df)
		return concate_df

	def drop_center_rows_dupblicates(self):
		df = self.concate_df()
		for prefix_from in self.prefix_from:
			try:
				df = df.drop(df[df["to"] == prefix_from + "cent"].index)
			except:
				None
		return df

	def set_null_distance_to_rows_dupblicates(self):
		df = self.concate_df()
		return df

	def _get_filtred_df(self, df):
		df = df.filter(NetworkPressureConstants.filtered_columns)
		return df

	def get_filter_concate_df(self):
		filtred_df = self._get_filtred_df(self.concate_df())
		return filtred_df
