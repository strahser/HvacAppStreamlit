from AnalyticalTables.AnalyticalControls.PivotAndGroupTableControl import *
from SQL.SqlControl.SqlQueryViewTableControl import *
from SQL.SqlModel.SqlConnector import SqlConnector
from InputView.InputViewControl import InputViewControl


class AnalyticalTableControl:
	"""read sql table for analytic"""

	def __init__(self, upload_layout: UploadLayout, connector=SqlConnector.conn_sql,key=""):
		self.upload_layout = upload_layout
		self.connector = connector
		self.key = key
		with st.sidebar:
			choose_group_table_or_sql = st.radio(
				"Choose Group Table or SQL Create", ["SQL Show View", "Group Table View"]
			)
		if choose_group_table_or_sql == "Group Table View":
			input_view_control = InputViewControl(self.upload_layout,self.key)
			all_tables = input_view_control.create_input_view()
			if isinstance(all_tables,pd.core.frame.DataFrame):
				self.pivot_and_group_table = PivotAndGroupTableControl()
				self.pivot_and_group_table.create_pivot_and_group_table(all_tables)
		if choose_group_table_or_sql == "SQL Show View":
			sql_view_table = SqlQueryViewTableControl(self.upload_layout, key=f"choose_group_table_or_sql{self.key}")
			sql_view_table.create_all_query_view()

