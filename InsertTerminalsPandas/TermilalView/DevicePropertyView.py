from InsertTerminalsPandas.InputData.input import *
from SQL.SqlModel.SqlConnector import SqlConnector
from InsertTerminalsPandas.Controls.AddSelectedDataToDBControl import AddSelectedDataToDBControl
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
import streamlit as st


class DevicePropertyView:
	counter = 0

	def __init__(self, system_, input_data_df: InputDataDF) -> None:
		self.input_data_df = input_data_df
		self.db_system_name = system_
		self.system_ = system_.title().replace('_', ' ')
		DevicePropertyView.counter += 1
		self.key_fild_system = self.system_
		self.directive_length = None
		self.directive_terminals = None
		self.device_area = None
		self.calculation_options = None
		self.ceiling_offset = None
		self.wall_offset = None
		self.single_device_orientation = None
		self.device_orientation_option2 = None
		self.device_orientation_option1 = None
		self.family_device_name = None

	def get_terminal_layout(self):
		orientation_list = self.input_data_df.device_orientation.orientation
		single_orientation_list = self.input_data_df.device_orientation.single_orientation.dropna()
		option_list = self.input_data_df.calculation_options
		column = st.columns(3)
		with column[0]:
			st.subheader('Terminal Type')
			self.type_index = st.selectbox('Select default terminal data',
			                               self.input_data_df.device_type[
				                               ColumnChoosing.type_index].unique(),
			                               key=f'type_index {self.key_fild_system}')

			self.family_device_name = st.selectbox('select terminal',
			                                       self.input_data_df.unique_terminals,
			                                       index=self._get_default_index(self.input_data_df.unique_terminals,
			                                                                     ColumnChoosing.family_device_name),
			                                       key=f'family_device_name {self.key_fild_system}')
			self.add_row_checkbox = st.checkbox("ADD Row To DB?",
			                                    help=f"""
			                                    You can replace data in db (excel sheet) terminal type 												
												""",
			                                    key=f'add_row_checkbox {self.key_fild_system}')
			if self.add_row_checkbox:
				self.new_type_index = st.text_input("New Type Index", value=self.type_index,
				                                    key=f'new_type_index {self.key_fild_system}')

			setattr(self,
			        f'button {self.key_fild_system}',
			        st.button(f"Replace Data in Table {self.key_fild_system}",
			                  key=f'button {self.key_fild_system}'))

		with column[1]:
			st.subheader('Terminal Geometry')
			self.device_orientation_option1 = st.selectbox('select orientation option1',
			                                               orientation_list,
			                                               index=self._get_default_index(
				                                               orientation_list,
				                                               "device_orientation_option1"),
			                                               key=f'device_orientation_option1 {self.key_fild_system} '
			                                               )

			self.device_orientation_option2 = st.selectbox('select orientation option2',
			                                               orientation_list,
			                                               index=self._get_default_index(
				                                               orientation_list,
				                                               "device_orientation_option2"),
			                                               key=f'device_orientation_option2 {self.key_fild_system} '
			                                               )

			self.single_device_orientation = st.selectbox('single terminal orientation',
			                                              single_orientation_list,
			                                              index=self._get_default_index(
				                                              single_orientation_list,
				                                              "single_device_orientation"),
			                                              key=f'single_device_orientation {self.key_fild_system} '
			                                              )

			self.wall_offset = st.number_input('wall offset', min_value=0,
			                                   value=self._check_default_integer_index("wall_offset"),
			                                   key=f'wall offset {self.key_fild_system}')
			self.ceiling_offset = st.number_input('ceiling offset', min_value=0,
			                                      value=self._check_default_integer_index("ceiling_offset"),
			                                      key=f'ceiling_offset {self.key_fild_system} '
			                                      )
		with column[2]:
			st.subheader('Calculation option')
			self.calculation_options = st.selectbox('choose calculation option',
			                                        option_list,
			                                        index=self._get_default_index(
				                                        option_list,
				                                        "calculation_options"),

			                                        key=f'choose calculation option {self.key_fild_system} '
			                                        )
			self.device_area = st.number_input('device area', min_value=0,
			                                   value=self._check_default_integer_index("device_area"),
			                                   key=f'device_area  {self.key_fild_system} '
			                                   )

			self.directive_terminals = st.number_input('directive device', min_value=0,
			                                           value=self._check_default_integer_index("directive_terminals"),
			                                           key=f'directive_terminals  {self.key_fild_system} '
			                                           )

			self.directive_length = st.number_input('directive length', min_value=0,
			                                        value=self._check_default_integer_index("directive_length"),
			                                        key=f'directive_length  {self.key_fild_system} '
			                                        )
		if getattr(self, f'button {self.key_fild_system}'):
			new_type_index = self.new_type_index if hasattr(self, "new_type_index") else None
			db_control = AddSelectedDataToDBControl()
			db_control.add_device_data_new_row_to_db(self, new_type_index)

	def _get_filter_data_from_db(self, column_name: str, default_terminal_data=None) -> str | int:
		default_terminal_data = self.type_index if not default_terminal_data else default_terminal_data
		con = SqlConnector.conn_sql
		q = f"select * from device_type where {ColumnChoosing.type_index} = '{default_terminal_data}' limit 1"
		return pd.read_sql_query(q, con).to_dict("records")[0][column_name]

	def _check_default_integer_index(self, column_name: str, default_terminal_data=None):
		filtered_data = self._get_filter_data_from_db(column_name, default_terminal_data)
		if filtered_data:
			try:
				return int(filtered_data)
			except:
				return 0
		else:
			return 0

	def _get_default_index(self, value_list: list, search_value: str):
		value_list = list(value_list)
		res = self._get_filter_data_from_db(search_value)

		if res in value_list:
			return value_list.index(res)
		else:
			return 0
