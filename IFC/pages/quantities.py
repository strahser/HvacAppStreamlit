import pandas as pd
import streamlit as st
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.pset
import ifcopenshell.geom

import StaticData.AppConfig
from IFC.IFCViews.IFCExample import create_example
from SQL.SqlView.AddSQLTableView import AddSQLTableView
from Session.StatementConfig import StatementConstants
from library_hvac_app.streamlit_custom_functions import AggGridOptions
from IFC.tools import ifchelper, pandashelper, graph_maker
from ifcopenshell import util
from SQL.SqlModel.SqlConnector import SqlConnector

session = st.session_state


def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def load_data():
    if "ifc_file" in session:
        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True
    else:
        session["ifc_file"] = {}


def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame


def create_ifc(wall):
    new_ifc = ifcopenshell.file()
    new_ifc.add(wall)
    st.write(ifcopenshell.util.element.get_psets(wall))
    new_ifc.write("new_wall.ifc")


def load_data_graph():
    if "ifc_file" in session:
        session.Graphs = {
            "objects_graph": graph_maker.get_elements_graph(session.ifc_file),
            "high_frquency_graph": graph_maker.get_high_frequency_entities_graph(session.ifc_file)
        }
        session["isHealthDataLoaded"] = True


def draw_graphs():
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        graph1 = session.Graphs["objects_graph"]
        st.pyplot(graph1)
    with row1_col2:
        graph2 = session.Graphs["high_frquency_graph"]
        st.pyplot(graph2)


def drop_empty_columns(selected_row_df: pd.DataFrame):
    selected_df = pd.DataFrame(selected_row_df.dropna(axis=1, how="all"))
    selected_row_df_column = "_selectedRowNodeInfo"
    if selected_row_df_column in selected_df.columns:
        selected_df = selected_df.drop(selected_row_df_column, axis=1)
        st.write(selected_df)
        return selected_df
    else:
        st.write(selected_df)
        return selected_df


def quantities_execute():
    st.header("🧮 Model Quantities")
    if "IsDataFrameLoaded" not in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:
        tab1, tab2, tab3 = st.tabs(["Dataframe Utilities", "Quantities Review", "Example"])
        with tab1:
            # DATAFRAME REVIEW
            st.header("DataFrame Review")
            # st.write(session.DataFrame)
            df_agg = AggGridOptions(session.DataFrame)
            selected_row = pd.DataFrame(df_agg.create_ag_selected_row_df("selected_rows"))
            st.subheader("Selected Data")
            updated_selected_df = drop_empty_columns(selected_row)
            key = f"{StaticData.AppConfig.MenuChapters.ifc_dash_board} data view"
            col1, col2, col3 = st.columns(3)
            if not updated_selected_df.empty:
                _new_table_name = col1.text_input("Enter New View Table Name", value="ifc_table",
                                                  key=f"new_view_table_name {key}")
                _category_name = col1.text_input("Enter New Category Table Name", value="ifc",
                                                 key=f"new_view_category_name {key}")
                _create_table_db_button = col1.button("Create Table DB", key=f"create_table_db button {key}")
                _all_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
                if _create_table_db_button:
                    try:
                        if StatementConstants.ifc_category not in st.session_state[StatementConstants.table_db].keys():
                            st.session_state[StatementConstants.table_db][_category_name] = []
                        _ifc_category_list = st.session_state[StatementConstants.table_db][_category_name]
                        updated_selected_df.to_sql(name=_new_table_name, con=SqlConnector.conn_sql, if_exists="replace")
                        _ifc_category_list.append(_new_table_name)
                        _all_tables.append(_new_table_name)
                        st.success(f"DB {_new_table_name} created")
                    except Exception as e:
                        st.warning(e)

        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector = st.selectbox("Select Class", session.Classes, key="class_selector")
                    session["filtered_frame"] = pandashelper.filter_dataframe_per_class(session.DataFrame,
                                                                                        session.class_selector)
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("Select Quantity Set", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Select Quantity", quantities, key="quantity_selector")
                        st.radio('Split per', ['Level', 'Type'], key="split_options")
                    else:
                        st.warning("No Quantities to Look at !")
            load_data_graph()
            draw_graphs()
            ## DRAW FRAME
            with row2col2:
                if "quantity_selector" in session and session.quantity_selector == "Count":
                    total = pandashelper.get_total(session.filtered_frame)
                    st.write(f"The total number of {session.class_selector} is {total}")
                else:
                    if session.qtos is not None:
                        st.subheader(f"{session.class_selector} {session.quantity_selector}")
                        graph = graph_maker.load_graph(
                            session.filtered_frame,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options,
                        )
                        st.plotly_chart(graph)
        with tab3:
            create_example()
    else:
        st.header("Step 1: Load a file from the Home Page")
