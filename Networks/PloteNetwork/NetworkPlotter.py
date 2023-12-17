
from Networks.CalculationNetwork.NetworkBuilder import *
from Polygons.PolygonPlot.PolygonPlotter import PolygonPlotter
from Polygons.PolygonPlot.MPLSetting import *
from library_hvac_app.list_custom_functions import to_list


class NetworkPlotter(PolygonPlotter):

	def __init__(
			self,
			polygon_merge: PolygonMerge,
			network_list: list,
			df_network,
			space_name: str = 'S_ID',  # todo replace S_ID
			show_grid: bool = True,
			is_filled: bool = False,
			title_prefix: str = ''
	):
		"""create layout with routes, from input list of df

        Args:
            polygon_merge (PolygonMerge): inst of polygon merge
            df_network (list): inst of NetworkBuilder.df_network
            system_location_point (tuple): unic sys point for all df
            sys_flow_column (str): unic sys_flow_column for all df
            system_name (str): unic system_name for all df
            space_name(str): for add text to spaces
            show_grid (bool, optional): _description_. Defaults to True.
            is_filled (bool, optional): _description_. Defaults to False.
            Example:
            polygon_merge = PolygonMerge(df,json_path,'S_sup_name','S_level','Этаж 01')
            
            network_builder1 = NetworkBuilder(
            polygon_merge = polygon_merge,
            system_location_point =  (20000,0),
            system_name = 'S01',
            sys_flow_column ='S_SA_fresh',
            network_coordinate_x = (-25000,25000),
            network_coordinate_y = (3000,3000),
            route_name= 'm_1')

            network_plotter = NetworkPlotter(
            polygon_merge = polygon_merge,
            df_network = df_list,
            system_location_point = network_builder1_1.system_location_point,
            sys_flow_column = network_builder1_1.sys_flow_column,
            system_name = network_builder1_1.system_name
            )
        """
		super().__init__(polygon_merge, show_grid)
		self.network_list = to_list(network_list)
		self.df_network = df_network
		self.sys_flow_column = network_list[0].sys_flow_column
		self.system_name = network_list[0].system_name
		self.space_name = space_name
		self.is_filled = is_filled
		self.title_prefix = title_prefix

	def get_intersection_column_name(self, df_network):
		"""choose column name from df (check vertical or horizontal orientation)"""
		if "y_cross_x" in df_network.columns:
			self.cross_x = "y_cross_x"
			self.cross_y = "y_cross_y"
		else:
			self.cross_x = "x_cross_x"
			self.cross_y = "x_cross_y"

	def add_location_point(self):
		for loc_point in self.network_list:
			self.ax.scatter(
				loc_point.system_location_point[0],
				loc_point.system_location_point[1],
				s=150, c="b"
			)

			self.ax.text(
				loc_point.system_location_point[0],
				loc_point.system_location_point[1],
				loc_point.route_name,
				fontsize=12
			)

	def draw_branches(self, df_network):
		x_branch = (df_network["pcx"], df_network[self.cross_x])
		y_branch = (df_network["pcy"], df_network[self.cross_y])
		self.ax.plot(
			x_branch,
			y_branch,
			color="r",
			linewidth=3,
		)

	def draw_main_routs(self, df_network):
		x_main = df_network[self.cross_x]
		y_main = df_network[self.cross_y]
		self.ax.plot(
			x_main,
			y_main,
			color="g",
			linewidth=7,
			linestyle="-.",
		)

	def add_text_to_branches(self, df_network):

		self.add_text_from_df(
			df_network,
			"pcx",
			"pcy",
			['L', ""],
			['', ""],
			[self.sys_flow_column, self.space_name],
			bbox=box_2,
			**text_style,
		)

	def add_text_to_main_routs(self, df_network):
		self.add_text_from_df(
			df_network,
			self.cross_x,
			self.cross_y,
			['', "L"],
			['', ""],
			['m_idx', "sum_column"],
			bbox=box_1,
			**text_style,
		)

	def add_title(self):
		self.ax.set_title(
			f"{self.title_prefix} {self.level_val} System {self.system_name}.",
			fontsize=20,
			style="italic",
			weight="bold",
		)

	def calculate(self) -> plt.figure:
		for df_network in self.df_network:
			self.get_intersection_column_name(df_network)
			self.add_location_point(),
			self.draw_branches(df_network),
			self.draw_main_routs(df_network)
			self.add_text_to_branches(df_network)
			self.add_text_to_main_routs(df_network)
			self.add_title()
		self.plot_polygons("", [], is_filled=self.is_filled)
		return self.fig
