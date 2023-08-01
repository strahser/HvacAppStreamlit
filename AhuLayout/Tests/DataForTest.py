import os
import inspect
import sys
from AhuLayout.Layouts.AHUConstruct import *
from AhuLayout.Layouts.ExportLayouts import *
import streamlit as st
from DataForTest import *
from AhuLayout.config import HtmlConfig


def add_path_to_folder():
	current_dir = os.path.dirname(
		os.path.abspath(inspect.getfile(inspect.currentframe()))
	)
	parent_dir = os.path.dirname(current_dir)
	root_dir = os.path.dirname(parent_dir)
	directory_list = [parent_dir, root_dir]
	for directory in directory_list:
		if directory not in sys.path:
			sys.path.insert(0, directory)


add_path_to_folder()

suply_system_name = "S02"
concate_df = ConcatExcelSheets(
	ReadExcelData.input_excel_AHU,
	ReadExcelData.to_revit_init,
	ahu_system_names=AhuData.ahu_systems_names,
)
ahu_equipment = AHUCreateEquipmentNameDict(concate_df, AhuData, HtmlConfig)
filtred_equipment = (
	ahu_equipment.create_dictionary_of_system_type_and_system_property()[
		suply_system_name
	]
)
exchanger_property = ExchangerProperty(ReadExcelData.settings)
ahu_construct = AHUConstructor(concate_df.concat_df(), exchanger_property, AhuData)
ahu_merge_blocks = AHUMergeBlocks(ReadExcelData, ahu_construct)

ahu_construct.add_exchange_names()
data_for_layout = DataForLayout(
	ahu_equipment, ahu_merge_blocks, suply_system_name, AhuData
)
