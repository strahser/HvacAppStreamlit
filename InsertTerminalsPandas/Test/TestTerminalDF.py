import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
sys.path.insert(0, root_dir) 
from InsertTerminalsPandas.MainDF import *
level_value = 'Этаж 01'
system_type = 'Supply_system'
divice_data = [
"up","up","center",100,100,"ADSK_Диффузор_Круглый_Вытяжной",4,"minimum_terminals",2,
]
device_property_columns_names = [
        'device_orientation_option1',
        'device_orientation_option2',
        'single_device_orientation',
        'wall_offset',
        'celing_offset',
        'family_device_name',
        'device_area',
        'calculation_options',
        'derective_terminals'
        ]
filtred_data = FilteredData(['837891','837892'],divice_data)
terminal_filter = AddFilteredCalculatedPointsToDF(level_value, system_type, filtred_data)
df_filter =terminal_filter.add_polygon_and_points_to_df()


print(df_filter.calculation_options)