from SQL.SqlControl.SqlCRUDOperationControl import *
from SQL.SqlView.TableAddDataView import *


class SqlTableToolsControl:
	"""create CRUD SQL Operations """
	def __init__(self,
	             init_df: pd.DataFrame,
	             filtered_df: pd.DataFrame,
	             table_name: str,
	             ):
		"""init_df for view columns,filtered_df for select id, table_name for SQL """
		self._init_df = init_df
		self._filtered_df = filtered_df
		self._sql_crud_control = SqlCRUDOperationControl(table_name)
		self._table_add_data_view = TableAddDataView(self._init_df)
		
	def create_crud_operation(self):
		self._create_checkboxes()
		self._create_column()
		self._delete_column()
		self._add_data_to_column()
		
	def _create_checkboxes(self):
		with st.expander("SQL Tolls"):
			self._create_column_checkbox = st.checkbox("Add Column?")
			self._add_data_to_column_checkbox = st.checkbox("Add Data to Column?")
			self._delete_column_checkbox = st.checkbox("Delete Column?")
			self._table_add_data_view.update_view()
				
	def _create_column(self):
		if self._create_column_checkbox:
			self._table_add_data_view.create_column_view()
			self._sql_crud_control.create_column(self._table_add_data_view)

	def _delete_column(self):
		if self._delete_column_checkbox:
			self._table_add_data_view.delete_column_view()
			self._sql_crud_control.drop_column(self._table_add_data_view)
			
	def _add_data_to_column(self):
		if self._add_data_to_column_checkbox:
			self._table_add_data_view.add_data_to_column_view()
			_filtered_df = self._get_filtered_df_id()
			self._sql_crud_control.add_data_to_column(_filtered_df, self._table_add_data_view)
		
	def _get_filtered_df_id(self):
		"""concat agg table checkboxes"""
		if not self._filtered_df.empty:
			_filtered_df = self._filtered_df[self._table_add_data_view.id_column].to_list()
			_filtered_df = [str(val) for val in _filtered_df if val]
			return _filtered_df
		else:
			return []