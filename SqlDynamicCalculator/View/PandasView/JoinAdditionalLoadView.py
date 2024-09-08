from SqlDynamicCalculator.Models.PandasModels.GroupByDfModel import *

from InputView.InputView import *
from SqlDynamicCalculator.Models.PandasModels.InputViewModel import *


class JoinBalanceType:
	def __init__(self, balance_type: BalanceTypeList, balance_model_data: GroupByDfModel.create_config_model):
		self.balance_type = balance_type
		self.balance_model_data = balance_model_data
		self.condition = self.balance_type.balance_name == str(self.balance_model_data.balance_type_selected)

	def add_balance_name_to_model_data(self):
		condition = self.balance_type.balance_name == str(self.balance_model_data.balance_type_selected)
		if condition:
			self.balance_type.balance_data.append(self.balance_model_data)

	def add_table_name(self):
		table_label = st.text_input("Enter  table label",
		                            value=self.balance_model_data.df_new_table_name,
		                            key=f"table_label {self.balance_model_data.df_new_table_name}",
		                            help="Enter the name of the table to be exported to excel")
		self.balance_model_data.df_table_label = table_label
		return table_label

	def _get_default_index(self, select_space_data) -> int:
		if self.balance_model_data and self.balance_model_data.df_joined_column_name in select_space_data.columns:
			default_index = select_space_data.columns.to_list().index(self.balance_model_data.df_joined_column_name)
			return default_index
		else:
			default_index = select_space_data.columns.to_list().index(0)
			return default_index

	def _get_space_data_joined_id(self, select_space_data):
		default_index = self._get_default_index(select_space_data)
		space_data_joined_id = st.selectbox(
			"Selected Columns for join space data",
			select_space_data.columns,
			index=default_index,
			key=f"input_space_data_joined_id {self.balance_model_data.df_new_table_name}",
			help="Select to be exported to excel"
		)
		return space_data_joined_id

	def _get_default_columns(self, select_space_data) -> list[str]:
		default_columns = st.multiselect("Select default columns in space data table",
		                                 options=select_space_data.columns.to_list(),
		                                 default=select_space_data.columns.to_list(),
		                                 key=f"default_columns {self.balance_model_data.df_new_table_name}")
		self.balance_model_data.default_columns = default_columns
		return default_columns

	def create_join_table(self, select_space_data):
		col1, col2 = st.columns([2, 8])
		with col1:
			space_data_joined_id = self._get_space_data_joined_id(select_space_data)
		with col2:
			default_columns = self._get_default_columns(select_space_data)
			df_join: pd.DataFrame = select_space_data[default_columns].merge(
				self.balance_model_data.df_group_table_values,
				on=space_data_joined_id,
				how="left"
			)
		self.balance_model_data.df_space_joined_table_values = df_join
		return df_join
