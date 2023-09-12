
import streamlit as st
import pandas as pd
from SQL.SqlModel.SqlConnector import SqlConnector
from Session.StatementConfig import StatementConstants


class StatementCategoryModel:
	@staticmethod
	def __create_df_balance_view():
		df = pd.DataFrame(st.session_state[StatementConstants.view_sql_query_model]).T
		if StatementConstants.category_name in df.columns and StatementConstants.view_name in df.columns:
			group_df = df \
				.groupby([StatementConstants.category_name])[StatementConstants.view_name] \
				.agg(list) \
				.to_dict()
			return group_df

	@staticmethod
	def create_balance_view(conn=SqlConnector.conn_sql):
		group_df = StatementCategoryModel.__create_df_balance_view()

		if group_df:
			for balance_type, table_names in group_df.items():
				with st.expander(balance_type):
					for en, name in enumerate(table_names):
						st.markdown(f"#### {name} ")
						with st.expander("+"):
							try:
								st.write(
									pd.read_sql(f"select * from {name}", con=conn)
								)
							except Exception as e:
								st.warning(e)