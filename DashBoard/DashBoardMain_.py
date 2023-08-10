import pandas as pd
import streamlit as st
from DashBoard.DashBoardView.DFStaticTab import DFStaticTab
from InputView.InputViewControl import InputViewControl
from Polygons.PolygonView.SelectPlotView import SelectPlotView
from Polygons.PolygonsControl.PlotToolsPanel import show_selected_levels
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import MenuChapters
from InputView.NodesView import ViewNodes
import pygwalker as pyg
import codecs
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
# pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip
import sweetviz as sv
import streamlit.components.v1 as components


from SQL.SqlModel.SqlConnector import SqlConnector


def loads_plots_from_session():
	with st.sidebar:
		select_plot_view = SelectPlotView(key=MenuChapters.dash_board)
		select_plot_view.create_checkboxes_plot_view()
	try:
		show_selected_levels(select_plot_view.selected_levels)

	except Exception as e:
		st.warning(e)


def _create_input_sql_tools_view(upload_layout, key):
	"""get selected sheet name"""
	input_view_control = InputViewControl(upload_layout, key)
	input_view_control.create_input_view()
	table_name = input_view_control.sheet_name
	return table_name


def dashboard_main(upload_layout):
	pd_profile, tableau, tab_static = st.tabs(["Profile", "Tableau", "Static"])
	with tab_static:
		table_view_node = ViewNodes(f"{MenuChapters.dash_board} Table")
		table_view_node.create_tree_view_options("Table")
		table_view_node_tree = table_view_node.table_tree
		if table_view_node_tree:
			tabs = st.tabs(table_view_node_tree)
			for en, tab in enumerate(tabs):
				with tab:
					try:
						charter_tab = DFStaticTab(table_view_node_tree[en], MenuChapters.dash_board)
						with st.expander(":heavy_plus_sign: Description Data"):
							charter_tab.create_static_view()
						with st.expander(f":heavy_plus_sign: Pivot Data"):
							charter_tab.create_pivot_df_view()
						with st.expander(f":heavy_plus_sign: AGG Detail Data"):
							tabs_agg = st.tabs(charter_tab.character_df_view.agg_data)
							for agg, tab_agg in zip(charter_tab.character_df_view.agg_data, tabs_agg):
								with tab_agg:
									with st.expander(f":heavy_plus_sign: :blue[${agg.title()} $]"):
										charter_tab.create_dynamic_view(agg)
					except Exception as e:
						st.warning(e)
	with tableau:
		config = st.session_state[StatementConstants.tableau_config]
		table = _create_input_sql_tools_view(upload_layout, f"{MenuChapters.dash_board} tableau")
		st.session_state[StatementConstants.tableau_table] = table
		if _check_is_table_name_in_list_all_tables_all_views(table):
			if st.session_state[StatementConstants.tableau_table]:
				df = pd.read_sql(f"select * from {st.session_state[StatementConstants.tableau_table]}",
				                 con=SqlConnector.conn_sql)
				pyg.walk(df, env='Streamlit', dark='light', themeKey="vega", spec=config)
			code_area = st.text_area("Past tableau code data").replace('vis_spec = """', "").replace('"""', "")
			clipboard_button = st.button("ADD to buffer",
			                             key="clipboard button",
			                             help="""insert the code and block into the text and confirm by pressing the button""")
			clear_button = st.button("clear buffer state", key="clear button")
			if clipboard_button:
				st.session_state[StatementConstants.tableau_config] = code_area
			if clear_button:
				st.session_state[StatementConstants.tableau_config] = None

	with pd_profile:
		table_name = _create_input_sql_tools_view(upload_layout, f"{MenuChapters.dash_board} profile pandas")
		if table_name:
			df = pd.read_sql(f"select * from {table_name}",
			                 con=SqlConnector.conn_sql)
			try:
				show_report_button = st.button("Show Report",key="show report button")
				if show_report_button:
					pr = ProfileReport(df)
					st_profile_report(pr)
			except Exception as e:
				st.warning(e)


def _check_is_table_name_in_list_all_tables_all_views(table: str) -> bool:
	all_tables = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]
	all_views = st.session_state[StatementConstants.table_db][StatementConstants.all_tables_view]
	condition_table__checking = (table in all_tables)
	condition_view_checking = (table in all_views)
	return condition_table__checking or condition_view_checking

	loads_plots_from_session()
