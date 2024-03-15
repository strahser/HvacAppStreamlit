class StatementConstants:
	table_db = "table db"
	category_view_list = "category_view_list"
	category_dictionary = "category dictionary"
	without_category = "Without category"
	view_sql_query_model = 'view_sql_query_model'
	json_polygons = "json_polygons"
	sql_view_query = "sql_view_query"
	category_name = "balance_type"
	view_name = "view_name"
	view_comments = "view_comments"
	mainHydralitMenuComplex = "mainHydralitMenuComplex"
	selected_app = "selected_app"
	loading_file = "loading_file"
	previous_view = "previous_view"
	levels_plots = "levels_plots"
	SimpleNamespace = "SimpleNamespace"
	CardDimensions = "CardDimensions"
	select_join_table = "Select join table"
	all_tables_db = "all tables db"
	all_tables_view = "all tables view"
	tableau_config = "tableau_config"
	tableau_table = "tableau_table"
	ifc_category = "ifc"
	terminal_names_dict = "terminal_names_dict"
	ahu_names_dict = "ahu_names_dict"
	network_plots = "Network Plots"
	networks = "Networks"
	zones = 'zones'


class SettingConfig:
	excluding_list = [
		"button",
		"file_uploader",
		"uploaded_file",
		"array_buffer",
		"ifc_file",
		"Graphs",
		"SequenceData",
		"DataFrame",
		"filtered_frame",
		"Classes",
		"ifc_js_response",
		"BIMDebugProperties",
		"HealthData",
		StatementConstants.levels_plots,
		StatementConstants.SimpleNamespace,
		# StatementConstants.select_join_table,
		"streamlit_elements.core.callback.elements_callback_manager",
		"streamlit_elements.core.frame.elements_frame.demo"

	]
