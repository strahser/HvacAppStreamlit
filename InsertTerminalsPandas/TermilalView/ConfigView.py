from InsertTerminalsPandas.InputData.input import *
from InsertTerminalsPandas.TermilalView.ConfigColumnChoosingView import ConfigColumnChoosingView
from InsertTerminalsPandas.TermilalView.ConfigStaticView import LayoutOptions, LabelListStatic
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
import streamlit as st


class ConfigView:
	def __init__(self, input_data_df: InputDataDF,key):
		self.key =key
		self.input_data_df = input_data_df
		self.system_type = input_data_df.system_dictionary.keys()
		self.df_levels = input_data_df.revit_export[ColumnChoosing.S_level].unique()
		self.choose_plot_radio_option = None
		self.selected_df_data_id = None
		self.system_select = None
		self.plot_height = None
		self.plot_width = None
		self.level_value = None

	def create_config_tab(self):
		col1, col2, col3 = st.columns(3)
		with col1:
			st.subheader('Choose  Columns Options')
			column_confirm_checkbox = st.checkbox("confirm column choosing",key=f"{self.key} column_confirm_checkbox")
			column_choosing = ConfigColumnChoosingView(self.input_data_df.revit_export,key=self.key)
			if column_confirm_checkbox:
				for attr_ in LabelListStatic.attr_list:
					config_column_attr = getattr(column_choosing, attr_)
					setattr(ColumnChoosing, attr_, config_column_attr)
			with col2:
				st.subheader('Choose  System Options')
				self.system_select = st.multiselect('select system type', self.system_type,
				                                    default=list(self.system_type)[0])
				self.choose_plot_radio_option = st.radio('choose visualisation of one level or all levels',
				                                         (LayoutOptions.one_level,
				                                          LayoutOptions.all_levels,
				                                          LayoutOptions.detail_view)
				                                         )
				if self.choose_plot_radio_option == LayoutOptions.one_level or LayoutOptions.detail_view:
					self.level_value = st.selectbox('choose level', self.df_levels)
		with col3:
			st.subheader('Choose Plot dimension Options')
			self.plot_width = st.number_input('plot width', 10, step=5, value=20)
			self.plot_height = st.number_input('plot _height', 10, step=5, value=20)
