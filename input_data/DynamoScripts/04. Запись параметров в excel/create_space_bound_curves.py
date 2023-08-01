import sys
import os
import json

path_to_current_file =IN[0]
curent_dir = os.path.dirname(str(path_to_current_file))
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(os.path.dirname(str(path_to_current_file)))
s_id,px,py,pz,pcx,pcy = IN[1]
s_dict ={
        str(s_id[en]):
        {
        "px":px[en],
        "py":py[en],
        "pz":pz[en],
        "pcx":pcx[en],
        "pcy":pcy[en]
        }
    for en,i in enumerate(s_id)}
with open(curent_dir+"\polygon_data_file.json", "w") as write_file:
    json.dump(s_dict,write_file, indent = 4)
OUT = json.dumps(s_dict, indent = 4)




