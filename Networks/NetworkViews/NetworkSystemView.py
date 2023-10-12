import streamlit as st
import pandas as pd


class NetworkSystemView:
	"""create side layout for systems property"""

	def __init__(self, df: pd.DataFrame, input_settings_df: pd.DataFrame):
		self.df = df
		self.system_type = input_settings_df["system_type"].unique()
		self.system_type_choice = st.selectbox("choose system type", self.system_type)
		self.system_choice = st.selectbox("choose system column", df.columns)
		self.sys_flow_choice = st.selectbox("choose flow column", df.columns)
		self.level_column = st.selectbox("choose level column", df.columns)
		self.system_name_choice = st.selectbox("choose system", df[self.system_choice].unique())
		self.space_name = st.selectbox("Select additional space  name text", ["S_ID", "S_Name", "S_Number"], index=2)
		system_filter = df[self.system_choice] == self.system_name_choice
		self.level_list = df[system_filter][self.level_column].unique()
