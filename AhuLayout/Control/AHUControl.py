import pandas as pd
import streamlit as st
from PIL import Image
import os
import inspect
import sys

current_dir = os.path.dirname(
	os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from AhuLayout.Model.AHUModel import *
from AhuLayout.Model.TotalDataConsumptionModel import TotalDataConsumptionModel
from library_hvac_app.DbFunction.pandas_custom_function import df_html_format, df_to_excel_in_memory_simple
from library_hvac_app.streamlit_custom_functions import get_download_docx_in_memory, get_download_excel_data, AggGridOptions


class AHUHtmlConfig:
	path_to_template = os.path.join(parent_dir, "static", "A3_template.docx")
	tabs_names = ["AHU Data", "Pivot Table", "Download Config"]
	pictures_path = 'AhuLayout/static/'


class AHUControl:

	def __init__(self, revit_df: pd.DataFrame, df_setting: pd.DataFrame, input_excel_AHU: pd.DataFrame, key):
		self.df_revit = revit_df
		self.df_setting = df_setting
		self.input_excel_AHU = input_excel_AHU
		self.key = key
		self.ahu_data_tabs, self.pivot_table_tab, self.download_config_tab = st.tabs(AHUHtmlConfig.tabs_names)
		self.filtered_df = [k for k, v in self.input_excel_AHU.items() if "Result_index" in v.columns and k != 'Расчет']
		self.ahu_list = self._create_ahu_list()

	def _create_ahu_list(self):
		ahu_list_inst = ListAHUModel(self.input_excel_AHU)
		ahu_list = ahu_list_inst.create_ahu_list(self.df_setting)
		return ahu_list

	def _create_ahu_select_data_view(self) -> None:
		with st.container():
			col = st.columns(4)
			self.choosing_system_name = col[0].selectbox('choose ahu system', self.filtered_df,
			                                             key=f"{self.key} choosing_system_name")
			self.system_columns_name = col[1].multiselect('Choose supply system columns', self.df_revit.columns,
			                                              key=f"{self.key} system_columns_name")
			self.space_numbers_column_name = col[2].selectbox('Choose space column number',
			                                                  options=self.df_revit.columns,
			                                                  index=self.__get_default_column_index(
				                                                  self.df_revit.columns.to_list(), 'S_Number'),
			                                                  key=f"{self.key} space_numbers_column_name"
			                                                  )

	@staticmethod
	def __get_default_column_index(list_value: list, value: str):
		if value in list_value:
			return list_value.index(value)
		else:
			return 0


	def create_ahu_data_tab(self):
		with self.ahu_data_tabs:
			with st.container():
				self._create_ahu_select_data_view()
				ahu = [ahu for ahu in self.ahu_list if ahu.system_name == self.choosing_system_name][0]
				st.subheader("AHU Construction")
				ahu_labels = ahu.list_ahu_labels
				column_len = len(ahu_labels)
				col = st.columns(column_len)

			st.subheader("AHU equipment scheme")
			for i in range(column_len):
				image = Image.open(ahu.list_ahu_pictures[i])
				with col[i]:
					st.write(ahu_labels[i])
					st.write(i)
					st.image(image)
			st.dataframe(ahu.list_ahu_property.fillna(0).reset_index(drop=True))

	def _create_pivot_table_view(self):
		st.write("Pivot AHU Table")
		pivot_table = PivotTableAHUModel()
		pivot_list = []
		for ahu in self.ahu_list:
			spaces = pivot_table.get_ahu_pivot_table(ahu,
			                                         self.df_revit,
			                                         self.system_columns_name,
			                                         self.space_numbers_column_name)
			pivot_list.append(spaces)
			concat_pivot = pd.concat(pivot_list)
		try:
			st.markdown(concat_pivot.to_html(
				float_format=lambda x: '{:,.0f}'.format(x).replace(
					u',', u' ') if x > 1e3 else '{:,.2f}'.format(x)),
				unsafe_allow_html=True)
		except:
			st.warning("Please check input system data columns")
		return concat_pivot

	def _create_total_df_consumption(self, df_):
		st.subheader("Result for export")
		df_agg = AggGridOptions(df_, False)
		df_export = df_agg.create_ag_selected_row_df()
		st.session_state["df_data_ahu_load"] = df_export.to_dict()
		return df_export

	def create_pivot_tab(self):
		with self.pivot_table_tab:
			self.pivot_df = self._create_pivot_table_view()
			self.df_ = TotalDataConsumptionModel.create_margins_table_view(self.ahu_list)
			self._create_total_df_consumption(self.df_)

	def create_download_tab(self):
		with self.download_config_tab:
			col = st.columns(4)
			with col[0]:
				st.subheader("Enter Project Number")
				project_number = st.text_input("Input Project Number", value="PN-1-1-1", label_visibility="collapsed",key=self.key)
			with col[1]:
				st.subheader("Excel Tables ")
				buffer_list = df_to_excel_in_memory_simple([self.pivot_df, self.df_], ["pivot_df", "summary_table"])
				st.download_button(
					label=f'📥download pivot table ',
					data=buffer_list,
					file_name="Pivot_AHU_Table.xlsx"
				)
			with col[2]:
				st.subheader("AHU Data")
				get_download_docx_in_memory(self.ahu_list,
				                            AHUHtmlConfig.path_to_template,
				                            ContextAhuDictionary,
				                            InputTableLabels,
				                            project_number)
