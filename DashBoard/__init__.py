import os.path
import os, sys, inspect
from pathlib import Path
myDir = os.path.dirname(os.path.abspath(__file__))
parentDir = Path(__file__).parents[1]
root_dir = Path(__file__).parents[2]