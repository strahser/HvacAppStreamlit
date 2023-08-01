from PrincipalSchems.View.StaticView import *
from StaticData.AppConfig import MenuChapters


class PlotConfigView:
	def __init__(self, key):
		self.key = key

	def add_plot_size(self):
		self.plot_width = st.number_input("choose plot width", value=2000, key=f"{self.key} plot_width ")
		self.plot_height = st.number_input("choose plot height", value=2000, key=f"{self.key} plot_height ")
