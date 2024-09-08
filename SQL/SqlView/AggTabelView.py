import pandas as pd
import streamlit as st
from library_hvac_app.streamlit_custom_functions import AggGridOptions
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


class AggTabelView:
	def __init__(self, init_df: pd.DataFrame):
		self.init_df = init_df

	def create_filtered_table(self,key:str=None) -> pd.DataFrame:
		with st.container():  # agg table
			st.subheader("Input table data")
			agg_ = AggGridOptions(self.init_df,key=key)
			filtered_df = agg_.create_ag_selected_row_df("select")
			filtered_df = pd.DataFrame(filtered_df)
		return filtered_df