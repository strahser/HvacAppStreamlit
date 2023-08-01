from AnalyticalTables.AnalyticalView.View import *
from AnalyticalTables.AnalyticalModels.AnaliticalTableModel import *


class PivotTableControl:
	def __init__(self, df: pd.DataFrame):
		self.group_table_view = PivotTableView(df)
		self.df = df

	def get_pivot_table(self):
		pivot_table = get_pivot_table(
			self.df,
			self.group_table_view.group_field_pivot,
			self.group_table_view.agg_field_pivot,
			self.group_table_view.pivot_columns_multiselect,
			self.group_table_view.agg_funk_pivot
		)
		return pivot_table

	def show_pivot_table(self):
		st.subheader("Pivot table")
		st.dataframe(self.get_pivot_table())
