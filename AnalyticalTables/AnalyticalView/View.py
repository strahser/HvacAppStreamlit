import pandas as pd
import streamlit as st


class BaseView:
	def __init__(self, input_df: pd.DataFrame) -> None:
		self.revit_df = input_df


class GroupTableView(BaseView):
	def __init__(self, input_df: pd.DataFrame) -> None:
		super().__init__(input_df)
		self.group_field = st.multiselect(
			"select field for groups",
			self.revit_df.columns, key="GroupTableView group_field"
		)
		self.agg_field = st.multiselect(
			"select numeric agg field",
			self.revit_df.columns, key="GroupTableView agg_field"
		)
		agg_funk_data = ["sum", "describe", "count", "all"]
		self.agg_funk = st.selectbox("select agg function", agg_funk_data, key="GroupTableView agg_funk")


class PivotTableView(BaseView):
	def __init__(self, revit_df: pd.DataFrame) -> None:
		super().__init__(revit_df)
		self.group_field_pivot = st.multiselect(
			"select field for groups(index)", self.revit_df.columns
		)
		self.agg_field_pivot = st.multiselect(
			"select numeric agg field(values)",
			self.revit_df.select_dtypes("number").columns,
		)
		self.pivot_columns_multiselect = st.multiselect(
			"select field for columns ", self.revit_df.columns
		)
		agg_funk_data_pivot = ["sum", "min", "max", "count"]
		self.agg_funk_pivot = st.multiselect(
			"select agg function", agg_funk_data_pivot, default="count"
		)
