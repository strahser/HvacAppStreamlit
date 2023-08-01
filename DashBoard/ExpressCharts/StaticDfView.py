from DashBoard.ExpressCharts import StreamlitExpressChartsView
from DashBoard.ExpressCharts._TableControl import _TableControl
import streamlit as st


class StaticDfView(_TableControl):
	def __init__(self, express_chart_view: StreamlitExpressChartsView, key):
		super().__init__(express_chart_view, key)
		self.df_sum = self.df.groupby(self.select_keys_x, as_index=False).agg(self.select_keys_y).sum()
		self.df_describe = self.df.groupby(self.select_keys_x)[self.select_keys_y].describe()

	def create_static_df_view(self):
		st.title(f"DF Property {self.header}")
		st.subheader("Native Df")
		st.write(self.df)
		col = st.columns([2, 4])
		with col[0]:
			st.subheader("DF Sum")
			st.write(self.df_sum)
		with col[1]:
			st.subheader("DF Describe")
			st.write(self.df_describe)
