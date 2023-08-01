import os
import sys

path_to_current_file = IN[0]
json_path = str(UnwrapElement(IN[1]))

curent_dir = os.path.dirname(str(path_to_current_file))
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(os.path.dirname(str(path_to_current_file)))

OUT = ParseJson(ReadJson(json_path).get_json_data()[0]).sys_flow_parametr_name
# OUT = ParseJson(ReadeJson(json_path).get_json_data()[1]).instance_points
# OUT = FamilyType('ADSK_Диффузор_Круглый_Приточный','ДП_250').get_filtred_family_type()