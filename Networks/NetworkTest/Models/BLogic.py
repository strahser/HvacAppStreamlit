import streamlit as st
from Networks.plote_polygons.PolygonMerge import PolygonMerge
from Session.StatementConfig import StatementConstants
session_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
json_polygons = st.session_state[StatementConstants.json_polygons]

def get_polygons():
    polygons = PolygonMerge(session_tables,json_polygons,
                            "S_sup_name",
                            "S_level",
                            "Этаж 01")
    st.write(polygons.merge_df())
    return polygons.make_level_filter()