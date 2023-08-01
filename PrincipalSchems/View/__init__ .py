import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
polygons = os.path.join(parent_dir,"Polygons")
library = os.path.join(parent_dir,"library_hvac_app")
sys.path.insert(0, parent_dir) 
sys.path.insert(0, root_dir) 
sys.path.insert(0, polygons)
