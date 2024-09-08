from InputView.InputViewModel.InputViewLoadDFfromStatment import create_input_choosing_data_form
from InsertTerminalsPandas.Controls.CreateAllViewsControl import *
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import ExcelSheetsLoads
from Upload.UploadLayout import UploadLayout


def insert_terminals_main(upload_layout: UploadLayout,key):
	input_data_df = InputDataDF(upload_layout)
	input_data_df.show_form()
	loaded_form = create_input_choosing_data_form(
		input_data_df,
		StatementConstants.terminal_names_dict,
		ExcelSheetsLoads.excel_sheet_names_Terminal
	)
	if loaded_form:
		input_data_df.create_config_data()
		main_ = CreateAllViewsControl(input_data_df, key)
		main_.choose_level_options()
	else:
		st.warning("Check Data")