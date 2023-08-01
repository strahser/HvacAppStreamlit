
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.pset
import ifcopenshell.geom
import pandas as pd
from ifcopenshell import util
import ifcopenshell.geom
import streamlit as st
import numpy as np

def create_example():
	"""https://blenderbim.org/docs-python/ifcopenshell-python/code_examples.html#get-all-door-occurrences-of-a-type"""
	def _create_df(ifc_types):
		df_list=[]
		for type_ in ifc_types:
			df_list.append(pd.DataFrame(ifcopenshell.util.element.get_psets(type_)))
		st.write(pd.concat(df_list).reset_index())

	session = st.session_state
	ifc = session["ifc_file"]
	ifc_class = st.selectbox("IFC Types",set(i.is_a() for i in ifc))
	st.subheader("Type property")
	with st.expander(":heavy_plus_sign:"):
		try:
			ifc_types = ifc.by_type(ifc_class)
			ifc_type = ifc_types[0]

			pset_qto = util.pset.PsetQto("IFC4")
			st.write(f"quantity of {ifc_class}" ,len(ifc_types))
			st.write("Dictionary of attributes (first element):")# Gives us a dictionary of attributes
			st.write(f"{ifc_class} Name: {ifc_type.Name}")
			st.write(ifc_type.get_info())
			# Get only properties and not quantities
			st.write(f"{ifc_class} property", ifcopenshell.util.element.get_psets(ifc_type, psets_only=True))
			# Get only quantities and not properties
			st.write(f"{ifc_class} quantities",ifcopenshell.util.element.get_psets(ifc_type, qtos_only=True))
			st.write("all applicable psets/qtos names for a certain class :",pset_qto.get_applicable_names("IfcMaterial"))
		except Exception as e:
			st.warning(e)
		try:
			st.write("location:",ifcopenshell.util.element.get_container(ifc_type))
			st.write("location Name:", ifcopenshell.util.element.get_container(ifc_type).Name)
		except Exception as e:
			st.warning(e)
	st.subheader("Create All elements Type property DF")
	with st.expander(":heavy_plus_sign:"):
		_create_df(ifc_types)
	st.subheader("Create one elements Type property")
	with st.expander(":heavy_plus_sign:"):
		st.write(ifcopenshell.util.element.get_psets(ifc_types[0]))
	try:
		settings = ifcopenshell.geom.settings()
		shape = ifcopenshell.geom.create_shape(settings, ifc_type)
		faces = shape.geometry.faces  # Indices of vertices per triangle face e.g. [f1v1, f1v2, f1v3, f2v1, f2v2, f2v3, ...]
		verts = shape.geometry.verts  # X Y Z of vertices in flattened list e.g. [v1x, v1y, v1z, v2x, v2y, v2z, ...]
		materials = shape.geometry.materials  # Material names and colour style information that are relevant to this shape
		material_ids = shape.geometry.material_ids  # Indices of material applied per triangle face e.g. [f1m, f2m, ...]
		# Since the lists are flattened, you may prefer to group them per face like so depending on your geometry kernel
		grouped_verts = np.array([[verts[i], verts[i + 1], verts[i + 2]] for i in range(0, len(verts), 3)])
		grouped_faces= np.array([[faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)])
		geom_dict = dict(
		shape=shape,
		faces=faces,
		verts=verts,
		materials=materials,
		material_ids=material_ids,
		grouped_verts=grouped_verts,
		grouped_faces =grouped_faces,
		)
		st.subheader("Geometry Data")
		with st.expander(":heavy_plus_sign:"):
			st.json(geom_dict)


	except Exception as e:
		st.warning(e)