import pandas as pd
from plotly import graph_objs as go


class PlotPlotlyUtils:
	@staticmethod
	def show_only_unique_legend(fig):
		names = set()
		fig.for_each_trace(
			lambda trace: trace.update(showlegend=False)
			if (trace.name in names)
			else names.add(trace.name)
		)
		return fig

	@staticmethod
	def add_text_to_plot(fig: go.Figure, _df: pd.DataFrame) -> None:
		# add text to center polygon. _df- df with text(TextWorkerForPlot)
		fig.add_trace(
			go.Scatter(
				x=_df["pcx"],
				y=_df["pcy"],
				mode="text",
				textfont=dict(size=14, family="Issocuper", color="black"),
				text="<em>" + _df["text"] + "</em>",
				texttemplate="%{text}",
				legendgroup="Space Text",
				name="Space Text",
				showlegend=False,
				hovertemplate="Space Text"
			)
		)
	@staticmethod
	def get_clicked_filter(clicked_filter_id_list: list[str]) -> list[str]:
		"""return id to type str"""
		if clicked_filter_id_list:
			return [str(val) for val in clicked_filter_id_list]
		else:
			return []
