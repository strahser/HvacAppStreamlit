import inspect
import os
import sys


def add_path_to_os():
	current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	parent_dir = os.path.dirname(current_dir)
	root_dir = os.path.dirname(parent_dir)
	sys.path.insert(0, current_dir)
	sys.path.insert(0, parent_dir)
	sys.path.insert(0, root_dir)
