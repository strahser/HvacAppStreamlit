import pandas as pd
import streamlit as st


class PlotView:
	def __init__(self, selected_excel_sheet: pd.DataFrame, key):
		self.revit_df = selected_excel_sheet
		self.key = key

	def get_plot_layout(self):
		fill_color_radio_col, level_choose_column, prefix_col = st.columns(3)
		with fill_color_radio_col:
			st.subheader("Color Options")
			self.color_filter_name = st.selectbox(
				"select color filter column", self.revit_df.columns,
				key=f"{self.key} polygon_plotter_select_color_filter_column",
				help="""select the column whose data will be displayed in color on all levels of the building"""
			)
			self.unique_table_id = st.selectbox(
				"select table unique id", self.revit_df.columns,
				key=f"{self.key} unique_table_id",
				help="""select the table id (space id)"""
			)
			self.is_need_fill_color = st.radio("Is need space fill color", (
				"space fill color", "Do not use color"),
			                                   horizontal=True,
			                                   key=f"{self.key} is_need_fill_color",
			                                   help="""
				Is need space fill color - fill spaces by data values\n
				Do not use color filter -without color filling
				"""
			                                   )

		with level_choose_column:
			st.subheader("Level Options")
			self.level_column_name = st.selectbox(
				"select level column",
				self.revit_df.columns,
				index=self.__preselect_level_column_name(),
				key=f"{self.key} polygon_plotter_select_level_column"
			)

		with prefix_col:
			st.subheader("Text Options")
			self._add_text_value_to_spaces()

	def __preselect_level_column_name(self):
		if "S_level" in self.revit_df.columns:
			idx = self.revit_df.columns.to_list().index("S_level")
			return idx
		else:
			return 0

	def _add_text_value_to_spaces(self):
		self.space_value = st.multiselect("Select Space Data", self.revit_df.columns,
		                                  key=f"{self.key} polygon_plotter_select_space_value", help="""
		                                  select the columns with the data that should be displayed in spaces
		                                  """
		                                  )
		self.space_prefix = st.text_input("select prefix", key=f"{self.key} polygon_plotter_select prefix")
		self.space_suffix = st.text_input("select suffix", key=f"{self.key} polygon_plotter_select suffix")
