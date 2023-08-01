import sys
import os
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitNodes")
clr.AddReference("DSCoreNodes")
clr.AddReference("DSOffice")
clr.AddReference('RevitAPI')
clr.AddReference("RevitServices")
import Revit
import Autodesk
import RevitServices
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
# Import Element wrapper extension methods
clr.ImportExtensions(Revit.Elements)
from DSCore.List import Flatten
from DSCore import Math
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.DB import *
from Autodesk.DesignScript.Geometry import *
import itertools as it
import json

doc = DocumentManager.Instance.CurrentDBDocument
def open_json(config_file):
    with open(config_file,"rb") as f:
        data = f.read().decode("utf -8")
    data_js = json.loads(data)
    return data_js
    
def DS_fam_insert_by_point(family, point):
    point = tolist(point)
    family_inst = [Revit.Elements.FamilyInstance.ByPoint(
        family, p) for p in point]
    return family_inst

def tolist(obj1):
    if hasattr(obj1, "__iter__"):
        return obj1
    else:
        return [obj1]

def DS_GPVBN(element, par_name):
    if hasattr(element, "__iter__"):
        parameter_value = [i.GetParameterValueByName(
            par_name) for i in element]
    else:
        parameter_value = element.GetParameterValueByName(par_name)
    return parameter_value


def DS_SPVBN(element, par_name, par_values):
    element = tolist(element)
    parameter_value = [Revit.Elements.Element.SetParameterByName(
        el, par_name, par_values) for el in element]
    return parameter_value


def repeate_val_list(val, repeat_list):
    result2 = []
    for v, r in zip(val, repeat_list):
        result = [v for v in it.repeat(v, r)]
        result2.append(result)
    return result2


def repeate_val(val, number):
    result = it.repeat(val, number)
    return result


def to_revit_points(DS_points):
    DS_points = tolist(DS_points)
    xyz = []
    for i in DS_points:
        point = i.ToXyz()
        xyz.append(point)

    return xyz


def r_NewFamilyInstance_by_point(points, family):
    family = UnwrapElement(family)
    points = to_revit_points(points)
    TransactionManager.Instance.EnsureInTransaction(doc)
    family_insert = [doc.Create.NewFamilyInstance(
        p, family, Structure.StructuralType.NonStructural) for p in points]
    TransactionManager.Instance.TransactionTaskDone()
    return family_insert


def checkParameter(param):
    for p in param:
        internal = p.Definition
        if internal.BuiltInParameter != BuiltInParameter.INVALID:
            return p
    return param[0]


def r_SetParameters(element, name, values):
    """
    set double value in element, int parameter in element.
    element:list, name -string, values -any (not list)
    """

    if isinstance(element, list):
        element = element
    else:
        element = [element]

    parameters = []
    listout = []

    for e in element:
        param = e.GetParameters(name)
        if len(param) == 0:
            parameters.append(None)
        else:
            p = checkParameter(param)
            parameters.append(p)

    TransactionManager.Instance.EnsureInTransaction(doc)
    for i, p in enumerate(parameters):
        if p is None:
            listout.append(None)
        elif p.StorageType == StorageType.Double:
            ProjectUnits = p.DisplayUnitType
            newval = UnitUtils.ConvertToInternalUnits(values, ProjectUnits)
            p.Set(newval)
            listout.append(element[i])
        elif p.StorageType == StorageType.ElementId:
            newval = values
            p.Set(newval.Id)
            listout.append(element[i])
        else:
            p.Set(values)
            listout.append(element[i])
    TransactionManager.Instance.TransactionTaskDone()
    return listout


def r_getParam(element,param):
	value = []
	try:
		DB = element.GetParameters(param)
		for i in DB:
			if "Double" in str(i.StorageType): 
				# Metric Converstion
				value.append(i.AsDouble()*304.8)
			elif "Integer" in str(i.StorageType):
				value.append(i.AsInteger())
			elif "String" in str(i.StorageType):
				value.append(i.AsString())
			else:
				elemId =i.AsElementId()
				value.append(doc.GetElement(elemId))
	except:
		pass
	return value

def r_look_up_any(element,parameter):
	# test need
	p = element.LookupParameter(parameter)
	if p:
		# is not None
		st = p.StorageType.ToString()
		if st=='String':
			v = p.AsString()
		elif st=='Double':                
			v= UnitUtils.ConvertFromInternalUnits(p.AsDouble(), p.DisplayUnitType)
		elif st=='Integer':                
			v= UnitUtils.ConvertFromInternalUnits(p.AsInteger(), p.DisplayUnitType)
		elif st=='ElementId':
			v = p.AsElementId()
		elif st =='ValueString':
			v = p.AsValueString()
		else:
			v=""
			
	else:
		# v=None
		raise ValueError("no parameter_name")
	return v  