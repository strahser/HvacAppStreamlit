from dataclasses import dataclass, field
from dict_to_dataclass import DataclassFromDict, field_from_dict
from library_hvac_app.html.Layouts import make_grid
import streamlit as st
import pandas as pd
from SQL.SqlModel.SqlConnector import SqlConnector


@dataclass()
class CardDimensionsFunctions(DataclassFromDict):
	w: list[int] = field_from_dict()
	x: int = field_from_dict()
	y: int = field_from_dict()
	i: list[str] = field_from_dict()
	streamlit_function: object = None

	def get_streamlit_function(self):
		grid = make_grid(self.x, self.w)
		for en_x in range(self.x):
			with grid[0][en_x]:
				df = pd.read_sql(f"select * from {self.i[en_x]}", con=SqlConnector.conn_sql)
				st.write(df)
