import streamlit as st
import pandas as pd
from library_hvac_app.list_custom_functions import to_list


class NetworkMainViewComponents:
	def __init__(self, df_to_revit: pd.DataFrame, input_settings_df: dict, key: str):
		self.key = key
		self.df_to_revit = df_to_revit
		self.input_settings_df = input_settings_df
		self.choose_existing_or_new_system = st.sidebar.radio("Choose Create o Exist", ["New System", "Exist System"])
		self.tabs = st.tabs(["System Options", "Network config", "Results", "Downloads"])
		self.system_type = self.input_settings_df["medium_property"]["system_type"].unique()
		self.system_type_choice = None
		self.plot_width = None
		self.filtered_level_list = None
		self.all_levels = None
		self.space_name = None
		self.system_choice = None
		self.sys_flow_choice = None
		self.system_name_choice = None
		self.level_column = None
		self.plot_height = None

	def system_type_component(self):
		return st.selectbox("choose system type", to_list(self.system_type),
		                    key=f"system_type_choice {self.key}")

	def system_choice_component(self):
		return st.selectbox("choose system column", to_list(self.df_to_revit.columns),
		                    key=f"system_choice {self.key}")

	def system_name_choice_component(self, system_choice: str):
		return st.selectbox("choose system", self.df_to_revit[system_choice].unique(),
		                    key=f"system_name_choice {self.key}")

	def sys_flow_choice_component(self):
		return st.selectbox("choose flow column", to_list(self.df_to_revit.columns),
		                    key=f"sys_flow_choice {self.key}")

	def level_column_component(self):
		return st.selectbox("choose level column", to_list(self.df_to_revit.columns),
		                    key=f"level_column {self.key}")

	def space_name_component(self):
		return st.selectbox("Select additional space  name text", ["S_ID", "S_Name", "S_Number"], index=2,
		                    key=f"space_name {self.key}")  # todo delete hardcode

	def plot_width_component(self):
		return st.number_input("Plot Width", value=15, key=f"plot_width {self.key}")

	def plot_height_component(self):
		return st.number_input("Plot Height", value=15, step=1, key=f"plot_height {self.key}")

	def create_plots_button_component(self):
		return st.sidebar.button("Create Plots",
		                         key="create_plots button",
		                         )
