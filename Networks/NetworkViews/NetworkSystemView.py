import streamlit as st
import pandas as pd


class NetworkSystemView:
	"""create side layout for systems property"""

	def __init__(self, df: pd.DataFrame, input_settings_df: dict):
		self.df = df
		self.system_type = input_settings_df["medium_property"]["system_type"].unique()
		self.system_type_choice = st.selectbox("choose system type", self.system_type)
		self.system_choice = st.selectbox("choose system column", df.columns)
		self.sys_flow_choice = st.selectbox("choose flow column", df.columns)
		self.level_column = st.selectbox("choose level column", df.columns)
		self.system_name_choice = st.selectbox("choose system", df[self.system_choice].unique())
		self.space_name = st.selectbox("Select additional space  name text", ["S_ID", "S_Name", "S_Number"], index=2)#todo delete hardcode
		system_filter = df[self.system_choice] == self.system_name_choice
		self.level_list = df[system_filter][self.level_column].unique()
		columns_names = ["S_Name","from_branch","to_branch","distance"]
		df_ = [{"S_Name":[],"from_branch":[]}]
		df_["from_branch"] = df_["from_branch"].astype('category')
		self.level_df = st.data_editor(df_,
		                               column_config={
			                               "from_branch": st.column_config.SelectboxColumn(
				                               help="The category of the app",
				                               width="medium",
				                               options=[
					                               "📊 Data Exploration",
					                               "📈 Data Visualization",
					                               "🤖 LLM",
				                               ],
				                               required=True,
			                               )
		                               },
		                               )
