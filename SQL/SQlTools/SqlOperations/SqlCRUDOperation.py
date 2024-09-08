from SQL.SQlTools.View.SQLToolsView import SQLToolsView, st
from SQL.SqlModel.SqlConnector import SqlConnector
from SQL.SqlModel.SqlQueryModel import SqlQueryModel


class SqlCRUDOperation:
	def __init__(self, table_name: str, connector=SqlConnector.conn_sql):
		"""create sql CRUD mapping with UI.Add UI TableAddDataView"""
		self.sql_query = SqlQueryModel(table_name)
		self.connector = connector
		self.cursor = self.connector.cursor()
		self.table_name = table_name

	def update_input_date(self, table_add_data_view: SQLToolsView):
		if table_add_data_view.update_input_date:
			self.sql_query.df_read_sql()

	def create_column(self, table_add_data_view: SQLToolsView):
		if table_add_data_view.create_column_button:
			return self.sql_query.create_column(table_add_data_view.new_column_name, table_add_data_view.column_type)

	def add_data_to_column(self, filtered_df: list, table_add_data_view: SQLToolsView):
		# filtered_df -select row for change data in column
		if table_add_data_view.add_data_to_column_button and filtered_df:
			df = self.sql_query.df_read_sql()
			if "index" in df.columns:
				df.drop("index", axis=1, inplace=True)
			df[table_add_data_view.id_column] = df[table_add_data_view.id_column].astype(str)
			condition = df[table_add_data_view.id_column].astype(str).isin(filtered_df)
			df.loc[condition, table_add_data_view.changed_column] = table_add_data_view.new_column_value
			df.to_sql(self.sql_query.table_name, self.sql_query.conn, if_exists="replace", index=False)
			st.success("values added to table")
			return self.sql_query.df_read_sql()
		elif table_add_data_view.add_data_to_column_button:
			st.warning("Please choose filtered data in table")

	def drop_column(self, table_add_data_view: SQLToolsView):
		if table_add_data_view.delete_column_button:
			df = self.sql_query.df_read_sql()
			if "index" in df.columns:
				df.drop("index", axis=1, inplace=True)
			elif table_add_data_view.delete_column_name in df.columns:
				df = df.drop(table_add_data_view.delete_column_name, axis=1)
				st.success(f"column {table_add_data_view.delete_column_name} deleted ")
				df.to_sql(self.sql_query.table_name, self.sql_query.conn, if_exists="replace", index=False)
				return self.sql_query.df_read_sql()
			else:
				st.warning(f"column {table_add_data_view.delete_column_name} not deleted ")

	def update_sql(self, filtered_df, table_add_data_view):
		self.sql_query.update_sql(
			column_filter_name=table_add_data_view.id_column,
			filtered_val=tuple(filtered_df),
			column_update_name=table_add_data_view.changed_column,
			val=table_add_data_view.new_column_value,
		)
		return self.sql_query.df_read_sql()

	def delete_exist_table(self,table_name:str):
		with self.connector:
			self.cursor.execute(f'drop table if exists {table_name}')

	def delete_exist_View(self,table_name:str):
		with self.connector:
			self.cursor.execute(f'drop view if exists {table_name}')