from PIL import Image
import os
import inspect
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)


class HelpTab:
	marker_path = os.path.join(current_dir, "resorsers", "Custom Markers.png")
	with st.expander("Hide/Show Equipment Symbols"):
		image = Image.open(marker_path)
		st.image(image)
