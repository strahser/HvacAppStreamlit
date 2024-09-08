from SQL.SqlModel.SqlConnector import *
import pandas as pd
import streamlit as st


class SqlQueryModel:
	
	def __init__(self, table_name: str, conn: sqlite3.Connection = SqlConnector.conn_sql):
		self.table_name = table_name
		self.conn = conn
		self.cursor = self.conn.cursor()
	
	def create_table(self):
		""""
		create tabel with column default filtered_id_column
		"""
		try:
			res = self.df_read_sql()
		except:
			q = f"CREATE TABLE {self.table_name}(filtered_id_column TEXT);"
			with self.conn:
				self.cursor.execute(q)
		return self.cursor.fetchall()
	
	def drop_table(self):
		q = f"drop table if exists {self.table_name}"
		with self.conn:
			self.cursor.execute(q)
		return self.cursor.fetchall()
	
	def df_to_sql(self, _init_df: pd.DataFrame) -> object:
		return _init_df.to_sql(name=self.table_name, con=self.conn, if_exists="replace", index=False)
	
	def df_read_sql(self) -> pd.DataFrame:
		res = pd.read_sql_query(sql=f"""select * from {self.table_name}""", con=self.conn)
		return res
	
	def create_column(self, column_name: str, column_type=str):
		try:
			with self.conn:
				self.cursor.execute(
					f"""
				ALTER TABLE {self.table_name}
				ADD COLUMN {column_name} {column_type}
				""")
			st.success(f"for table {self.table_name} colum {column_name} created")
			return self.df_read_sql()
		except Exception as e:
			st.write(e)
	
	def insert_value(self, column_name, value):
		q = f"INSERT INTO {self.table_name} ({column_name}) VALUES({value})"
		
		with self.conn:
			self.cursor.execute(q)
		return self.df_read_sql()
	
	def update_sql(self, column_filter_name: str, filtered_val: list, column_update_name: str, val):
		"""
			add data to column
			with conn_sql:
			cur = conn_sql.cursor()
			q =
			update init_df
			SET test_column1 = "some values"
			cur.viewer_execute(q)
			"""
		
		with self.conn:
			
			cur = self.conn.cursor()
			if isinstance(val, str):
				q = f"""update {self.table_name} 
						SET {column_update_name} = "{val}"					
						WHERE {column_filter_name} in {filtered_val}; """
			else:
				q = f"""update {self.table_name} 
						SET {column_update_name} = {val}				
						WHERE {column_filter_name} in {filtered_val}; """
			print(q)
