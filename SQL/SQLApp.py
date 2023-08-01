from SQL.SqlControl.SqlDataSelectAndUpdateControl import SqlDataSelectAndUpdateControl
import pandas as pd


def main_sql_app(input_df: pd.DataFrame, table_name: str):
	sql_tool = SqlDataSelectAndUpdateControl(input_df, table_name)
	selected_table_value = sql_tool.create_agg_table()
	return selected_table_value