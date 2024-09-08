from Upload.UploadLayout import *
from Polygons.PolygonView.PlotView import *
import matplotlib.pyplot as plt


class PolygonMPLControl:
	def __init__(self, upload_layout: UploadLayout) -> None:
		self.plot_view = PlotView(upload_layout.revit_export)
		self.plot_view.get_plot_layout()
		self.upload_layout = upload_layout
	
	def _create_plot_figures_all_levels(self) -> tuple[list[plt.Figure], list[str]]:
		all_plots = []
		all_save_plots = []
		for level_val in self.plot_view.revit_df[self.plot_view.level_column_name].unique():
			fig_temp, save_fig_temp = create_plot(
				self.upload_layout.revit_export,
				self.upload_layout.json_file,
				self.plot_view.color_filter_name,
				self.plot_view.level_column_name,
				level_val,
				self.plot_view.space_prefix,
				self.plot_view.space_suffix,
				self.plot_view.space_value,
			)
			all_plots.append(fig_temp)
			all_save_plots.append(save_fig_temp)
		return all_plots, all_save_plots
	
	def legend_without_duplicate_labels_fig(self, figure, legenda_font_size):
		handles, labels = plt.gca().get_legend_handles_labels()
		by_label = dict(zip(labels, handles))
		figure.legend(by_label.values(), by_label.keys(), fontsize=legenda_font_size)
	
	def show_plots(self, legenda_font_size=14) -> None:
		all_plots, save_plots = self._create_plot_figures_all_levels()
		with st.expander("ALL Plot"):
			for fig_ in all_plots:
				self.legend_without_duplicate_labels_fig(fig_, legenda_font_size)
				st.pyplot(fig_)
