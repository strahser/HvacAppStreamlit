import pandas as pd
import streamlit as st

from DashBoard.Components.CardDimensions import CardDimensions
from DashBoard.Components.CardDimensionsFunctions import CardDimensionsFunctions
from Session.StatementConfig import StatementConstants


def create_st_dashboard():
	dataclass_instance = [CardDimensions.from_dict(val) for val in
	                      st.session_state[StatementConstants.CardDimensions]]
	df = pd.DataFrame(dataclass_instance)
	df = df.groupby("y").agg({"x": "count", "w": lambda x: list(x), "i": lambda x: list(x)}).reset_index()
	dataclass_functions = [CardDimensionsFunctions.from_dict(val) for val in df.to_dict("records")]
	dataclass_functions_update = [val.get_streamlit_function() for val in dataclass_functions]