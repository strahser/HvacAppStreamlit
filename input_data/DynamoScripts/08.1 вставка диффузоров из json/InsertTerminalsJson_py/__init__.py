# -*- coding: utf-8 -*- 
import sys
import os
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from Autodesk.Revit.DB.Structure import *
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
clr.AddReference('RevitNodes')
# импорт и работа с геометрией Dynamo
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
doc = DocumentManager.Instance.CurrentDBDocument
