import dataclasses
import inspect

import pandas as pd
import streamlit as st
from dataclasses import dataclass, asdict, fields

from Session.StatementConfig import StatementConstants


@dataclass
class PlotViewAttributes:
	color_filter_name: str = None
	unique_table_id: str = None
	level_column_name: str = None
	is_need_fill_color: bool = None
	space_value: list[str] = None
	space_prefix: str = None
	space_suffix: str = None


class PlotViewComponents(PlotViewAttributes):
	# if StatementConstants.zones not in st.session_state:
	# 	st.session_state[StatementConstants.zones]={}
	zones = st.session_state[StatementConstants.zones]

	def __init__(self, revit_df: pd.DataFrame, key: str):
		self.revit_df = revit_df
		self.key = key

	@staticmethod
	def indices(l: list, val: any) -> int:
		"""Always returns a list containing the indices of val in the_list"""
		res = [index for index, value in enumerate(l) if value == val]
		return res[0] if res else 0

	def load_from_session(self, key):
		col_list = self.revit_df.columns.to_list()
		try:
			res = self.indices(col_list, self.zones.get(key))
			return res
		except:
			return 0

	def color_filter_name_component(self):
		key = f"{self.key} color_filter_name"
		return st.selectbox(
			"select color filter column", self.revit_df.columns,
			index=self.load_from_session('color_filter_name'),
			key=key,
			help="""select the column whose data will be displayed in color on all levels of the building"""
		)

	def unique_table_id_component(self):
		return st.selectbox(
			"select table unique id", self.revit_df.columns,
			key=f"{self.key} unique_table_id",
			index=self.load_from_session('unique_table_id'),
			help="""select the table id (space id)"""
		)

	def level_column_name_component(self):
		return st.selectbox(
			"select level column",
			self.revit_df.columns,
			index=self.__preselect_level_column_name(),
			key=f"{self.key} level_column_name"
		)

	def is_need_fill_color_component(self):
		return st.radio("Is need space fill color", (
			"space fill color", "Do not use color"),
		                horizontal=True,
		                key=f"{self.key} is_need_fill_color",
		                help="""
				Is need space fill color - fill spaces by data values\n
				Do not use color filter -without color filling
				""")

	def space_value_component(self):
		st_values = self.zones.get('space_value')
		default_values = st_values if st_values and set(st_values).issubset(set(self.revit_df.columns)) else []
		return st.multiselect("Select Space Data", self.revit_df.columns,
		                      key=f"{self.key} space_value",
		                      default=default_values,
		                      help="""
		                            select the columns with the data that should be displayed in spaces
		                            """
		                      )

	def space_prefix_component(self):
		return st.text_input("select prefix", key=f"{self.key} space_prefix")

	def space_suffix_component(self):
		return st.text_input("select suffix", key=f"{self.key} space_suffix")

	def __preselect_level_column_name(self):
		if "S_level" in self.revit_df.columns:
			idx = self.revit_df.columns.to_list().index("S_level")
			return idx
		else:
			return 0


class PlotView(PlotViewComponents):
	annotated_text = PlotViewAttributes.__annotations__.keys()

	def __init__(self, revit_df: pd.DataFrame, key):
		super().__init__(revit_df, key)

	def get_plot_layout(self):
		session_zone_data = st.session_state[StatementConstants.zones]
		with st.form("Setting form"):
			fill_color_radio_col, level_choose_column, prefix_col = st.columns(3)
			with fill_color_radio_col:
				st.subheader("Color Options")
				self.color_filter_name = self.color_filter_name_component()
				self.unique_table_id = self.unique_table_id_component()
				self.is_need_fill_color = self.is_need_fill_color_component()

			with level_choose_column:
				st.subheader("Level Options")
				self.level_column_name = self.level_column_name_component()

			with prefix_col:
				st.subheader("Text Options")
				self.space_value = self.space_value_component()
				self.space_prefix = self.space_prefix_component()
				self.space_suffix = self.space_suffix_component()

			form_submit = st.form_submit_button('Submit')
			if form_submit:
				for val in self.annotated_text:
					attr_ = getattr(self, val)
					session_zone_data[val] = attr_
