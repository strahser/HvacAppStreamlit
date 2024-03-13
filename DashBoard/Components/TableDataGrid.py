from streamlit_elements import dashboard, mui, html, nivo
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd


def get_db_table(table_name: str):
	df = pd.read_sql(f"select * from {table_name}", con=SqlConnector.conn_sql)
	df["id"] = df.index
	columns = [{"field": col} for col in df.columns]
	rows = df.to_dict("records")
	return columns, rows


def _create_data_grid(table_name):
	columns, rows = get_db_table(table_name)
	mui.DataGrid(
		columns=columns,
		rows=rows,
		pageSize=5,
		rowsPerPageOptions=[6],
		checkboxSelection=True,
		disableSelectionOnClick=False,

	)
