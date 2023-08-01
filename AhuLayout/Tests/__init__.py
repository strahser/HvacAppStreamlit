import os
import inspect
import sys
def add_path_to_folder():
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(parent_dir)
    directory_list = [parent_dir,root_dir]
    for directory in directory_list:
        if directory not in sys.path:
            sys.path.insert(0, directory) 
add_path_to_folder()
