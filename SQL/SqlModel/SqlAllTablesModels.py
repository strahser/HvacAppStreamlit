from SQL.SqlModel.SqlConnector import *
import pandas as pd


class SqlAllTablesModels:
	__metaclass__ = Singleton
	tables = SqlConnector.conn_sql.cursor().execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
	table_name = set()
	
	@staticmethod
	def table_info():
		"""
	    prints out all the columns of every table in db
	    c : cursor object
	    conn : database connection object
	    """
		tables = SqlConnector.conn_sql.cursor().execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
		for table_name in tables:
			table_name = table_name[0]  # tables is a list of single item tuples
			table = pd.read_sql_query("SELECT * from {} LIMIT 0".format(table_name), SqlConnector.conn_sql)
			print(table_name)
			for col in table.columns:
				print('\t' + col)
			print()
