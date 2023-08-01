class StatementConstants:
	table_db = "table db"
	without_category = "Without category"
	create_json = 'create_json'
	sql_view_query = "sql_view_query"
	category_name = "balance_type"
	view_name = "view_name"
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
