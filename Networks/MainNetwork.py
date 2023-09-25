import os
import inspect
import streamlit
import sys

import SQL.SqlModel.SqlConnector
from Session.StatementConfig import StatementConstants

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)

from Upload.UploadLayout import UploadLayout
from Networks.ControlNetwork.NetworkPressureLayout import *


def create_network_plot():
	session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
	json_polygons = st.session_state[StatementConstants.json_polygons]
	condition = "revit_export" in session_tables and "medium_property" in session_tables and len(json_polygons)>1
	if condition:#todo add user interface
		revit_export = pd.read_sql(f"select * from revit_export",con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		medium_property = pd.read_sql(f"select * from medium_property",con=SQL.SqlModel.SqlConnector.SqlConnector.conn_sql)
		main_network = NetworkPressureLayout(
			revit_export,
			json_polygons,
			medium_property,
		)
		show_network = st.button("Show Network")
		if show_network:
			main_network.create_df_and_plot_layout()