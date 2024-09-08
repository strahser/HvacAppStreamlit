from Polygons.PolygonView.PlotView import *


class PlotlySelectByClickView:
	def __init__(self, init_df: pd.DataFrame, plot_view: PlotView):
		col = st.columns(3)
		self.all_levels = list(init_df[plot_view.level_column_name].unique())
		self.level_names = col[0].selectbox(
			"select level for filtration", self.all_levels, help="""
			select level which will be displayed below,\n 
			and you can select the data by clicking \n 
			the mouse and updating the layout\n 
		"""
		)
		self.id_for_color_filter = col[1].selectbox("select color id column name for clicked select",
		                                        init_df.columns,
		                                        help="""
		                                        select a column whose data will be displayed on the same
		                                        level
	                                        of the building and you can select them
	                                        """
		                                        )
		self.level_index = self.all_levels.index(self.level_names)
		self.clear_selected = st.button("clear selected", help="clear selected data")
		self.update = st.button("update layout", help="push to update layout")
