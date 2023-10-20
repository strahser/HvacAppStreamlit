from PrincipalSchems.View.DynamicBaseView import DynamicBaseView
from PrincipalSchems.View.StaticView import EquipmentSymbol


class DynamicEquipmentPropertyView(DynamicBaseView):
	def __init__(self, df_,key, columns_number) -> None:
		super().__init__(df_,key,columns_number)

	@staticmethod
	def __create_beautifully_number(row_flow: float):
		if isinstance(row_flow, float):
			split_number = "{0:,}".format(round(row_flow)).replace(",", " ")
			return split_number
		else:
			return row_flow

	def _equipment_config_add_label_to_layout(self):
		"""equipment config"""
		for en, val in enumerate(self.equipment_config_scheme_list):
			self.columns[en + 1].write(val)

	def add_level_widget_to_layout(
			self, unique_level_column_list: list, column_number=1
	):
		for ind, row in self.df_.iterrows():
			setattr(
				self,
				f"level_label_{row['system']}",
				self.columns[column_number].selectbox(
					"#",
					unique_level_column_list,
					key=f"{self.key} level_label_{row['system']}",
					label_visibility="collapsed",
				),
			)

	def add_flow_widget_to_layout(self, column_number=1):
		for ind, row in self.df_.iterrows():
			setattr(
				self,
				f"flow_label_{row['system']}",
				self.columns[column_number].text_input(
					label="#",
					value=f"L= {self.__create_beautifully_number(row['flow'])} m3/h",
					key=f"{self.key} flow_label_{row['system']}",
					label_visibility="collapsed",
				),
			)
	def _on_change_callback(self, row):
		return EquipmentSymbol.symbols[getattr(self, f"equipment_symbol_{row['system']}")]

	def __add_equipment_symbol(self, row, column_number):
		setattr(
			self,
			f"equipment_symbol_{row['system']}",
			self.columns[column_number].selectbox(
				"#",
				EquipmentSymbol.symbols.keys(),
				key=f"{self.key} equipment_symbol_{row['system']}",
				label_visibility="collapsed",
			),
		)

	def __add_equipment_label(self, row, column_number):
		setattr(
			self,
			f"equipment_label_{row['system']}",
			self.columns[column_number + 1].text_input(
				"#",
				key=f"{self.key} equipment_label_{row['system']}",
				label_visibility="collapsed",
				value=self._on_change_callback(row),
			),
		)

	def add_symbol_widget_to_layout(self, column_number=1):
		for ind, row in self.df_.iterrows():
			self.__add_equipment_symbol(row, column_number)
			self.__add_equipment_label(row, column_number)
