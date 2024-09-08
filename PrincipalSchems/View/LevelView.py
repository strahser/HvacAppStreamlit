import streamlit as st
import pandas as pd
from StaticData.AppConfig import MenuChapters


class LevelView():
	def __init__(self, df_: pd.DataFrame, key) -> None:
		self.level_column = None
		self.key = key
		self.df_ = df_

	def choose_level_column(self):
		self.level_column = st.selectbox(
			"select level column",
			self.df_.columns,
			key=f"{self.key} level_column ",
			index=self.__get_default_level_value())

	def __get_default_level_value(self):
		if "S_level" in self.df_.columns:
			return list(self.df_.columns.values).index("S_level")
		else:
			return 0
