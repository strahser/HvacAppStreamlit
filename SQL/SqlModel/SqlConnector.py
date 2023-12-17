import sqlite3


class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class SqlConnector(object):
	__metaclass__ = Singleton
	memory_connection_path = "file::memory:?cache=shared"
	conn_sql: sqlite3.Connection = sqlite3.connect(memory_connection_path, uri=True, check_same_thread=False)
	conn_local_sql: sqlite3.Connection = sqlite3.connect("./export_excel.db", check_same_thread=False)
