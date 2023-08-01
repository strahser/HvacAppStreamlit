from AnalyticalTables.AnalyticalControls.PivotTableControl import *


class GroupTableControl:
	def __init__(self, df: pd.DataFrame):
		self.group_table_view = GroupTableView(df)
		self.df = df

	def get_group_table_view(self):
		pass

	def get_group_table(self) -> pd.DataFrame:
		group_table = get_group_table(
			self.df,
			self.group_table_view.group_field,
			self.group_table_view.agg_field,
			self.group_table_view.agg_funk,
		)
		return group_table

	def show_group_table(self):
		st.subheader("Group Table")
		st.dataframe(self.get_group_table())
