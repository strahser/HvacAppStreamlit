from AnalyticalTables.AnalyticalView.View import *
from AnalyticalTables.AnalyticalModels.AnaliticalTableModel import *
from StaticData import CSS
from StaticData.CSS import CssStyle


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
		try:
			df_html = self.get_pivot_table().to_html(classes="table ")
			st.write(df_html,unsafe_allow_html=True)
		except Exception as e:
			st.warning(e)