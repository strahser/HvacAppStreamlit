from InsertTerminalsPandas.Controls.CreateAllViewsControl import *
from Upload.UploadLayout import UploadLayout


def insert_terminals_main(upload_layout: UploadLayout,key):
	input_data_df = InputDataDF(upload_layout)
	loaded_form = input_data_df.create_input_choosing_data_form()
	if loaded_form:
		input_data_df.create_config_data()
		main_ = CreateAllViewsControl(input_data_df, key)
		main_.choose_level_options()