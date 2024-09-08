# region import
import os
import inspect
import sys
import streamlit

current_dir = os.path.dirname(
	os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)

from AhuLayout.Model.AHUModel import *
# endregion

# region input data
path_ahu = os.path.join(parent_dir, "InputData", "calculation_AHU.xlsm")
path_revit = os.path.join(parent_dir, "InputData", "to_revit_init.xlsx")
path_setting = os.path.join(parent_dir, "InputData", "settings.xlsx")
system_columns_name = ['S_sup_name']
excel_ahu = pd.ExcelFile(path_ahu).sheet_names
df_revit: pd.DataFrame = pd.read_excel(path_revit)
df_ahu = pd.read_excel(path_ahu, skiprows=14, nrows=10, sheet_name=None)
df_setting = pd.read_excel(path_setting, sheet_name="medium_property")
# endregion

def save_to_docx(ahu_list):
	render_docx = RenderDocx(InputTableLabels)
	render_docx.create_or_open_docx_file("test.docx")
	for ahu in ahu_list:
		context_dictionary = ContextAhuDictionary()
		context_dictionary.system_name = ahu.system_name
		context_dictionary.ahu_equip_name = ahu.list_ahu_labels
		context_dictionary.ahu_pictures = ahu.list_ahu_pictures
		context_dictionary.ahu_property = ahu.list_ahu_property
		context_dictionary.ahu_excel_df = ahu.excel_df
		render_docx.add_context_to_file(context_dictionary)
	render_docx.save("test.docx")


if __name__ == '__main__':
	ahu_list_inst = ListAHUModel(df_ahu)
	ahu_list_inst.create_ahu_list(df_setting)
	pivot_table = PivotTableAHUModel()
	pivot_list = []
	for ahu in ahu_list_inst.list_ahu:
		spaces = pivot_table.get_ahu_pivot_table(ahu, df_revit, system_columns_name)
		pivot_list.append(spaces)
		concat_pivot = pd.concat(pivot_list)
	streamlit.write(concat_pivot)
