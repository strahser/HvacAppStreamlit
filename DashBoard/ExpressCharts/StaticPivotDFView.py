from io import StringIO

import pandas as pd
import  streamlit as st
from DashBoard.ExpressCharts import StreamlitExpressChartsView
from DashBoard.ExpressCharts._TableControl import _TableControl
from library_hvac_app.html.Layouts import make_grid


class StaticPivotDFView(_TableControl):
	def __init__(self, express_chart_view: StreamlitExpressChartsView, key):
		super().__init__(express_chart_view, key)
		self.getfunc_list = ["sum", "count", "mean"]
		self.pivot_tabs = st.tabs(self.getfunc_list)

	def create_pivot_dash(self):
		try:
			df_pivot_table = self._create_pivot_tabel()
			if df_pivot_table:
				for en, name, in enumerate(df_pivot_table):
					with self.pivot_tabs[en]:
						with st.expander(f":heavy_plus_sign: :blue[${name.title()} $]"):
							st.subheader(f"detail with agg function {name}")
							st.write(df_pivot_table[name])
							grid = make_grid(1, 2)
							bar = self._create_pd_plot(df_pivot_table[name], "bar", fig_size=(6, 8))
							line = self._create_pd_plot(df_pivot_table[name], "line", fig_size=(6, 8))
							with grid[0][0]:
								st.write(bar, unsafe_allow_html=True)
							with grid[0][1]:
								st.write(line, unsafe_allow_html=True)
			else:
				st.warning("Check Pivot Table Data")
		except Exception as e:
			st.warning(e)

	def _create_pivot_tabel(self) -> dict[str:pd.DataFrame]:
		if self.select_subgroup:
			df_subgroup = {}
			for agg in self.getfunc_list:
				df = pd.pivot_table(
					data=self.df,
					index=self.select_subgroup,
					values=self.select_keys_y,
					columns=self.select_keys_x,
					aggfunc=agg,
					margins=True,
					margins_name="Total"
				)
				df_subgroup[agg] = df
			return df_subgroup

	@staticmethod
	def _save_to_svg(fig):
		i = StringIO()
		fig.savefig(i, format="svg")
		return i.getvalue()

	def _create_pd_plot(self, df, plot_kind='bar', fig_size=(4, 4)):
		ax = df.plot(kind=plot_kind, figsize=fig_size)
		fig_ = ax.get_figure()
		svg_fig = self._save_to_svg(fig_)
		return svg_fig