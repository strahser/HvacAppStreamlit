import pandas as pd
import streamlit as st
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import ExcelSheetsLoads
from SQL.SqlModel.SqlConnector import SqlConnector


def create_input_choosing_data_form(object_: object, stat_constant_dict: str, excel_sheet_names_dict: str,
                                    connector=SqlConnector.conn_sql):
	checking_list = []
	if len(st.session_state[stat_constant_dict].keys()) == len(excel_sheet_names_dict):
		for key, value in st.session_state[StatementConstants.terminal_names_dict].items():
			if not isinstance(value, list):
				try:
					df = pd.read_sql(f"select * from {value}", con=connector)
					setattr(object_, key, df)
					checking_list.append(True)
				except Exception as e:
					st.write(e)
					checking_list.append(False)
			else:
				df_list = []
				for v in value:
					try:
						df = pd.read_sql(f"select * from {v}", con=connector)
						df_list.append(df)
						checking_list.append(True)
					except Exception as e:
						st.write(e)
						checking_list.append(False)
				setattr(object_, key, df_list)
		return all(checking_list)
	else:
		return False
