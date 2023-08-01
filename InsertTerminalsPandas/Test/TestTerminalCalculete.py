import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
sys.path.insert(0, root_dir) 
from InsertTerminalsPandas.Core.ChooseTerminalFromDBModel import *

space_flow = 24000
space_area = 200
system_type = 'Supply_system'
terminl_name = 'ADSK_Диффузор_Круглый_Приточный'
joined_table = JoinRevitExportTerminalsSheets(system_type)
terminals = ChooseTerminalsInstanceFromDB(
    InputDataDF.concate_base,terminl_name, space_flow)
[
"up",
"up",
"center",
100,
100,
"ADSK_Диффузор_Круглый_Вытяжной",
4,
"minimum_terminals",
2,
]

fiter_df = FilterEmptySpaceTerminalsInDF(system_type).make_filter_spaces_and_terminals_notnull()
terminals_calculated = CalculateSpaceTerminalsInDF(fiter_df,system_type)
terminal_filter = CalculateSpaceTerminalsInDF()

print(terminals_calculated.add_k_ef_and_device_flow_to_DF())