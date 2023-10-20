import streamlit as st

from Networks.NetworkModels.NetworkBranchModel import NetworkBranchModel, NetworkSystemModel
from Networks.plote_polygons.PolygonMerge import PolygonMerge
from Session.StatementConfig import StatementConstants

session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
json_polygons = st.session_state[StatementConstants.json_polygons]


def get_polygons():
	polygons = PolygonMerge(session_tables, json_polygons,
	                        "S_sup_name",
	                        "S_level",
	                        "Этаж 01")
	st.write(polygons.merge_df())
	return polygons.make_level_filter()


if __name__ == "__main__":
	n_branch = NetworkBranchModel("level", "drat plot", "pressure plot", "long_plot", )
	n_branch1 = NetworkBranchModel("level1", "drat plot", "pressure plot", "long_plot", )
	system = NetworkSystemModel("S1", "ventilation")
	system.add_branches(n_branch)
	system.add_branches(n_branch1)
	system.create_branch_name()
	print(system)
